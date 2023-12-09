class Chord:
    def __init__(self):
        # 半音階（シャープとフラットを含む）
        self.chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        # 根音（ルート音）と音符のマッピング
        self.note_map = {
            1: 'C',
            2: 'D',
            3: 'E',
            4: 'F',
            5: 'G',
            6: 'A',
            7: 'B'
        }

    def major_chord(self, root):
        # メジャーコードの間隔
        intervals = [0, 4, 7]
        return self._build_chord(root, intervals)

    def minor_chord(self, root):
        # マイナーコードの間隔
        intervals = [0, 3, 7]
        return self._build_chord(root, intervals)

    def augmented_chord(self, root):
        # 増和音コードの間隔
        intervals = [0, 4, 8]
        return self._build_chord(root, intervals)

    def diminished_chord(self, root):
        # 減和音コードの間隔
        intervals = [0, 3, 6]
        return self._build_chord(root, intervals)

    def dominant_seventh_chord(self, root):
        # ドミナントセブンスコードの間隔
        intervals = [0, 4, 7, 10]
        return self._build_chord(root, intervals)

    def major_seventh_chord(self, root):
        # メジャーセブンスコードの間隔
        intervals = [0, 4, 7, 11]
        return self._build_chord(root, intervals)

    def minor_seventh_chord(self, root):
        # マイナーセブンスコードの間隔
        intervals = [0, 3, 7, 10]
        return self._build_chord(root, intervals)

    def suspended_second_chord(self, root):
        # サスペンデッドセカンドコードの間隔
        intervals = [0, 2, 7]
        return self._build_chord(root, intervals)

    def suspended_fourth_chord(self, root):
        # サスペンデッドフォースコードの間隔
        intervals = [0, 5, 7]
        return self._build_chord(root, intervals)

    def _build_chord(self, root, intervals):
        # 根音からコードを構築
        root_note = self.note_map[root]
        root_index = self.chromatic_scale.index(root_note)
        chord_notes = [self.chromatic_scale[(root_index + interval) % 12] for interval in intervals]
        return chord_notes

"""
# 使用例
chord = Chord()
print(chord.major_chord(1))  # Cメジャーコード
print(chord.minor_chord(1))  # Cマイナーコード
print(chord.augmented_chord(1))  # C増和音コード
print(chord.diminished_chord(1))  # C減和音コード
print(chord.dominant_seventh_chord(1))  # C7コード
print(chord.major_seventh_chord(1))  # CM7コード
print(chord.suspended_second_chord(1))  # Csus2コード
print(chord.suspended_fourth_chord(1))  # Csus4コード
"""
