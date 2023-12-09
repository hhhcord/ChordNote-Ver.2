import re  # 正規表現を扱うためのモジュールをインポートします。
import os  # ファイルパスやディレクトリの操作を行うためのモジュールをインポートします。
import sys  # Pythonのインタプリタやシステム関連の機能を扱うためのモジュールをインポートします。
import argparse  # コマンドラインからの引数を解析するためのモジュールをインポートします。
from fractions import Fraction  # 分数を扱うためのモジュールをインポートします。
import music21  # 音楽データの分析や操作を行うためのライブラリmusic21をインポートします。
import pandas as pd  # データ分析やデータ操作を容易にするためのライブラリPandasをインポートします。

class CSVToMidiConverter:
    # MIDIファイルに変換する際に使用する音名とその数値表現のリストです。
    notes = ['C', 'D-', 'D', 'E-', 'E', 'F', 'G-', 'G', 'A-', 'A', 'B-', 'B']  
    # 音名からMIDIの数値に変換するための辞書です。
    note_to_num = {n: i for i, n in enumerate(notes)}  
    # 同じ音を表す異なる表記を整合させるための辞書です。
    same_note = {'A#': 'B-', 'C#': 'D-', 'D#': 'E-', 'F#': 'G-', 'G#': 'A-'}  

    @staticmethod
    def split_note(note):
        # 音符を音名とオクターブに分割する関数です。
        # 正しくフォーマットされていない場合はエラーを発生させます。
        assert re.fullmatch('[A-G](#|-)?[0-7]', note) is not None, 'Note not formatted correctly.'
        return note[:-1], int(note[-1])

    @staticmethod
    def name_to_num(name):
        # 音名をMIDIの数値に変換する関数です。
        # 音名とオクターブを分割し、数値に変換します。
        note, octave = CSVToMidiConverter.split_note(name)
        b = CSVToMidiConverter.note_to_num.get(CSVToMidiConverter.same_note.get(note, note))
        a = (octave + 1) * 12
        return a + b

    @staticmethod
    def produce_midi(filename, df, desired_tempo, output_dir_name):
        # MIDIファイルを生成する関数です。
        # 曲のテンポや音符の情報を設定してMIDIファイルを作成します。
        s1 = music21.stream.Stream()
        s1.append(music21.tempo.MetronomeMark(number=desired_tempo))
        running_offset = 0

        for _, row in df.iterrows():
            curr_duration = row.iloc[3]
            x = music21.note.Note(CSVToMidiConverter.name_to_num(row.iloc[1]), duration=music21.duration.Duration(Fraction(curr_duration)))
            x.volume.velocity = row.iloc[4]
            x.offset = row.iloc[2] + running_offset
            s1.insert(x)

        s1.write("midi", os.path.join(output_dir_name, filename[:-4] + ".mid"))

    @staticmethod
    def is_dir(dirname):
        # 引数がディレクトリかどうかをチェックする関数です。
        # ディレクトリでない場合はエラーを発生させます。
        if not os.path.isdir(dirname):
            raise argparse.ArgumentTypeError(f"{dirname} is not a directory")
        return dirname

    @staticmethod
    def process_directory(input_dir_name, output_dir_name=None, desired_tempo=None):
        # ディレクトリ内の全てのCSVファイルを処理してMIDIに変換する関数です。
        # 出力ディレクトリが指定されていない場合は入力ディレクトリの名前に基づいて作成します。
        if not output_dir_name: 
            output_dir_name = input_dir_name + "-output-midis"
        if not os.path.exists(output_dir_name):
            os.makedirs(output_dir_name)
        for file in os.listdir(input_dir_name):
            filename = os.fsdecode(file)
            df = pd.read_csv(os.path.join(input_dir_name, filename), engine='python')
            df_tempo = df.iloc[1,5] if desired_tempo is None else desired_tempo
            CSVToMidiConverter.produce_midi(filename, df, df_tempo, output_dir_name)

    @staticmethod
    def parse_arguments():
        # コマンドライン引数を解析する関数です。
        # 必要な引数やオプションを定義し、解析します。
        parser = argparse.ArgumentParser()
        parser.add_argument("input_dir_name", type=str)
        parser.add_argument("-o", "--output_dir_name", type=str)
        parser.add_argument("-t", "--tempo", type=int)
        return parser.parse_args()

    @staticmethod
    def main():
        # メイン関数です。
        # 引数を解析し、ディレクトリを処理してMIDIファイルを生成します。
        args = CSVToMidiConverter.parse_arguments()
        CSVToMidiConverter.is_dir(args.input_dir_name)
        CSVToMidiConverter.process_directory(args.input_dir_name, args.output_dir_name, args.tempo)

"""
# スクリプトが直接実行された場合にのみ main() を呼び出します
if __name__ == "__main__":
    CSVToMidiConverter.main()
"""
