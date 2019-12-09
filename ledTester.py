import RPi.GPIO as GPIO
import time

def main():
    print("[テスト前の確認]")
    print("")
    print("GPIO 13に緑LED - 通常稼働中")
    print("GPIO 19に黄LED - メッセージ処理中など")
    print("GPIO 26に赤LED - エラー発生など")
    print("GPIO 12にボタン - エラー表示のキャンセル")
    print()
    print("これらが正常に接続されていることを確認してください。")
    print("Enterキーを押すとテストが始まります。")
    print()

    input()
    
    try:
        print("------------------------------------------------------")
        print("準備しています。")
        print("  GPIOを使用するために設定を行っています。")
        GPIO.setmode(GPIO.BCM)
        print("  GPIOの予約を行っています。")
        print("    -- 13 Output")
        GPIO.setup(13, GPIO.OUT)
        print("    -- 19 Output")
        GPIO.setup(19, GPIO.OUT)
        print("    -- 26 Output")
        GPIO.setup(26, GPIO.OUT)
        print("    -- 12 Input")
        GPIO.setup(12, GPIO.IN)
        print("[1] 緑LEDの確認")
        print("  緑LEDが点灯していることを確認してください。")
        GPIO.output(13, GPIO.HIGH)
        input()
        GPIO.output(13, GPIO.LOW)
        print("[2] 黄LEDの確認")
        print("  黄LEDが点灯していることを確認してください。")
        GPIO.output(19, GPIO.HIGH)
        input()
        GPIO.output(19, GPIO.LOW)
        print("[3] 赤LEDの確認")
        print("  赤LEDが点灯していることを確認してください。")
        GPIO.output(26, GPIO.HIGH)
        input()
        GPIO.output(26, GPIO.LOW)
        print("[4] ボタンの確認")
        print("  ボタンを押してください。")
        while GPIO.input(12) == GPIO.LOW:
            time.sleep(0.1)

        print("  ボタンが押されました。")
        print("  正常に動作したことを確認してください。")
        input()
        print()
        print("全てのテストが完了しました。")
        print("正常に動作しなかった場合は、配線不良や接触不良を疑ってください。")
    except:
        import traceback
        traceback.print_exc()

        print("----------------")
        print("例外が発生しました。GPIOをクリーンして終了します。")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
