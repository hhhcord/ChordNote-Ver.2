# 音楽データを扱うためのクラスをインポート
from MusicDataHandler import MusicDataHandler
from Chord import Chord
from MusicProcessor import MusicProcessor
from CSVToMidiConverter import CSVToMidiConverter

# ユーザーに処理を選択させる
choice = input("どちらの処理を行いますか？\n1: コード進行のメモ\n2: MIDIにするためのcsvファイルの作成\n選択: ")

# 選択肢に応じて異なる処理を行う
if choice == '1':
    # 音楽データを扱うハンドラーを初期化
    handler = MusicDataHandler("music_data.csv")

    # 既存のデータを読み込む
    existing_data = handler.load_data()

    # ユーザーから新しいデータを入力してもらう
    new_data = handler.get_user_input()

    # 新しいデータを保存する
    handler.save_data(new_data)

    # 実演のため、既存のデータと新しいデータを表示する
    print(existing_data)
    print(new_data)
elif choice == '2':
    # コードと音楽処理用のクラスを初期化
    chord = Chord()
    music_processor = MusicProcessor(chord)

    # 行を選択
    row = input("読み込む行数を選択: ")

    # 音楽データを処理してMIDI用のcsvファイルを作成
    music_processor.process_music_data('music_data.csv', int(row))

    # MIDI ファイルの作成
    csv_to_midi_converter = CSVToMidiConverter
    CSVToMidiConverter.main()
    
else:
    # 不正な選択がされた場合にエラーメッセージを表示
    print("不正な選択です。")
