import csv

class MusicDataHandler:
    def __init__(self, filename):
        # コンストラクタ：ファイル名を受け取り、インスタンス変数に保存
        self.filename = filename

    def load_data(self):
        """CSVファイルから既存のデータを読み込む"""
        try:
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                data = [row for row in reader]
            return data
        except FileNotFoundError:
            # ファイルが見つからない場合は空のリストを返す
            return []

    def save_data(self, new_row):
        """CSVファイルに新しいデータを保存する"""
        with open(self.filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(new_row)

    def get_user_input(self):
        """新しいデータ行のためにユーザーから入力を受け取る"""
        comfort = self.get_integer_input("快適度 (-5 to 5): ", -5, 5)
        activity = self.get_integer_input("活性度 (-5 to 5): ", -5, 5)
        structure = self.get_structure_input("構造 (Intro, Verse, Chorus, Bridge, Outro): ")
        # キーの入力を取得
        key = self.get_key_input()

        # コードペアの数をユーザーに尋ねる
        chord_pairs = self.get_integer_input("ルートとコードのタイプの組は何組ですか？(4 または 8): ", 4, 8)

        chords = []
        for i in range(chord_pairs):
            root_num = self.get_integer_input(f"ルートの番号 {i+1} (1 to 7): ", 1, 7)
            chord_type = self.get_chord_type_input(f"M, m, aug, dim, 7th, M7th, m7th, sus2, sus4 の中からコードのタイプ {i+1} を選択: ")
            chords.extend([root_num, chord_type])

        # コードペアが4組の場合、残りのペアを0で埋める
        if chord_pairs == 4:
            chords.extend([0] * 8)

        return [comfort, activity, structure, key] + chords

    @staticmethod
    def get_integer_input(prompt, min_val, max_val):
        """ユーザーから指定された範囲の整数を入力してもらう"""
        while True:
            try:
                value = int(input(prompt))
                if min_val <= value <= max_val:
                    return value
                else:
                    print(f"入力は {min_val} から {max_val} の間でなければなりません。")
            except ValueError:
                print("有効な整数を入力してください。")

    @staticmethod
    def get_structure_input(prompt):
        """ユーザーから有効な構造入力を受け取る"""
        valid_structures = ["Intro", "Verse", "Chorus", "Bridge", "Outro"]
        while True:
            structure = input(prompt)
            if structure in valid_structures:
                return structure
            else:
                print("無効な構造。有効な選択肢: " + ", ".join(valid_structures))

    @staticmethod
    def get_key_input():
        """ユーザーから有効なキー入力を受け取る"""
        notes = ["A", "B", "C", "D", "E", "F", "G"]
        modifiers = ["", "#"]
        scales = ["Major", "Minor"]

        while True:
            note = input("キーの基本音名 (A to G): ")
            if note in notes:
                modifier = input("シャープ(#)を追加しますか？ (y/n): ")
                if modifier.lower() in ['y', 'n']:
                    scale = input("Major または Minor? ")
                    if scale in scales:
                        modifier = "#" if modifier.lower() == 'y' else ""
                        return note + modifier + " " + scale
                    else:
                        print("無効なスケール。有効な選択肢: Major, Minor")
                else:
                    print("無効な入力。'y' か 'n' を入力してください。")
            else:
                print("無効な音名。有効な選択肢: " + ", ".join(notes))

    @staticmethod
    def get_chord_type_input(prompt):
        """ユーザーから有効なコードタイプを受け取る"""
        chord_types = [
            "M", "m", "aug", "dim", "7th", "M7th", "m7th", "sus2", "sus4"
        ]
        while True:
            chord_type = input(prompt)
            if chord_type in chord_types:
                return chord_type
            else:
                print("無効なコードタイプ。有効な選択肢: " + ", ".join(chord_types))

'''
# Example usage
handler = MusicDataHandler("music_data.csv")

# 既存のデータを読み込む
existing_data = handler.load_data()

# ユーザーから新しいデータを入力してもらう
new_data = handler.get_user_input()

# 新しいデータを保存する
handler.save_data(new_data)

# デモンストレーションのために、既存のデータと新しいデータを表示
print(existing_data)
print(new_data)
'''
