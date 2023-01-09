from time import strftime
from kivy import Config

# a fixed size is set for the app's display when executed
Config.set("graphics", "height", "500")
Config.set("graphics", "width", "600")

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock

"""
#日本語入力する為のフォントを追加する　　　　　　　
from kivy.core.text import LabelBase, DEFAULT_FONT  # 追加分
from kivy.resources import resource_add_path  # 追加分
resource_add_path('c:/Windows/Fonts')  # 追加分
LabelBase.register(DEFAULT_FONT, 'msgothic.ttc')  # 追加分
"""


class ClockApp(MDApp):
    # Clock object for the clock(in the app) event
    event_clock = None

    def build(self):
        """
        メインスクリーンをビルドする
        """
        # マテリアルデザインのテーマカラーを決める
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Pink"

        return MainScreen()

    def on_start(self):
        """
        アプリ開始と同時に、クロックを作動する
        """

        self.event_clock = Clock.schedule_interval(self.root.clock_update, 1)


class MainScreen(MDScreen):
    #クロック処理を行うためのオブジェクト
    event_chrono = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.chrono_mins = 0
        self.chrono_secs = 0
        self.total_seconds = 0

    def clock_update(self, dt):
        """
        クロックに表示されている時間帯をアップデートするための関数。毎秒実行される
        """
        self.time_label.text = strftime('%H : %M : %S %p')

    def chrono_update(self, dt):
        """
        タイマーの時間をアップデートする
        """
        self.total_seconds += dt
        self.chrono_mins, self.chrono_secs = divmod(self.total_seconds, 60)
        self.ids.chrono_label.text = f" {str(int(self.chrono_mins)).zfill(2)} : {str(int(self.chrono_secs)).zfill(2)}.[size=30sp]{str(int((self.chrono_secs * 100) % 100)).zfill(2)}[/size]"


    def reset_chrono(self):
        """
        表示時間をリセットする。タイマーをストップしたときに使う。
        """
        self.event_chrono.cancel()
        self.ids.chrono_label.text = " 00 : 00.[size=30sp]00[/size]"
        self.total_seconds = 0
        #self.ids.start_stop_btn.text = "Start"
        self.ids.bottomBar.icon = "play"
        self.ids.bottomBar.icon_color = (0.3, 0.3, 0.7, 1)

    def start_stop_chrono(self):
        """
        タイマーを一時停止・再開
        """
        if self.ids.bottomBar.icon == "play":
            self.event_chrono = Clock.schedule_interval(self.chrono_update, 0.042)
            #self.ids.start_stop_btn.text = "stop"
            self.ids.bottomBar.icon = "stop"
            self.ids.bottomBar.icon_color = (0.9, 0.3, 0.3, 1)

        else:
            self.event_chrono.cancel()
            #self.ids.start_stop_btn.text = "Start"
            self.ids.bottomBar.icon = "play"
            self.ids.bottomBar.icon_color = (0.3, 0.3, 0.7, 1)



if __name__ == "__main__":
    from kivy.core.text import LabelBase

    LabelBase.register(
        name="OFont",
        fn_regular="Meslo LG/MesloLGL-Regular.ttf",
        fn_bold="Meslo LG/MesloLGL-Bold.ttf"
    )
    # Run the App

    ClockApp().run()