import os
import pandas as pd
from Chord import Chord

class MusicProcessor:
    def __init__(self, chord_class):
        # コードクラスを初期化
        self.chord_class = chord_class

    def process_music_data(self, file_path, row_number):
        # 指定されたCSVファイルからヘッダーなしで特定の行を読み込む
        music_data = pd.read_csv(file_path, header=None)
        row = music_data.iloc[row_number - 1]  # インデックスを0から始めるための調整

        # コード進行とその他の詳細を抽出
        comfort, activity, structure, key = row[0], row[1], row[2], row[3]
        chord_progression = row[4:].values

        # コード進行を処理して音符のシーケンスを生成
        notes = self._generate_notes(chord_progression)

        # 出力ファイル名を作成
        output_file_name = f"{comfort}_{activity}_{structure}_{key}.csv"

        # 出力ディレクトリのパス
        output_dir = './data/input'

        # ディレクトリが存在しない場合は作成
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 出力ファイルパスの設定
        output_file_path = os.path.join(output_dir, output_file_name)

        # 新しいCSVファイルにヘッダーとインデックスを付けて音符を出力
        pd.DataFrame(notes, columns=['note_name', 'start_time', 'duration', 'velocity', 'tempo']).to_csv(output_file_path, index_label='index')

    def _generate_notes(self, chord_progression):
        notes_data = []
        start_time = 0
        duration = 4  # 各コードが4拍続くと仮定
        velocity = 100  # 一定のベロシティを仮定
        tempo = 120  # 一定のテンポを仮定

        for i in range(0, len(chord_progression), 2):
            root, chord_type = chord_progression[i], chord_progression[i + 1]
            if root == 0:
                break  # コード進行の終わり

            # コードノートを生成
            chord_notes = self._get_chord_notes(root, chord_type)

            # コードの各ノートをノートデータに追加
            for note in chord_notes:
                note_name = note + '4'  # ハイフンなしのノートに4を追加
                notes_data.append([note_name, start_time, duration, velocity, tempo])

            start_time += duration  # 次のコードの開始時間へ移動

        return notes_data

    def _get_chord_notes(self, root, chord_type):
        chord_methods = {
            'M' : self.chord_class.major_chord,
            'm': self.chord_class.minor_chord,
            'aug': self.chord_class.augmented_chord,
            'dim' : self.chord_class.diminished_chord,
            '7th': self.chord_class.dominant_seventh_chord,
            'M7th': self.chord_class.major_seventh_chord,
            'm7th': self.chord_class.minor_seventh_chord,
            'sus2': self.chord_class.suspended_second_chord,
            'sus4': self.chord_class.suspended_fourth_chord,
        }
        return chord_methods[chord_type](root)

"""
# 例の使用方法
# chord = Chord()
# music_processor = MusicProcessor(chord)
# music_processor.process_music_data('music_data.csv', 1)
"""
