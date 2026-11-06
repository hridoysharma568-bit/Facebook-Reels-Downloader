import os
import yt_dlp
from httpcore import NetworkError
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp

kv = '''
MDScreen:
    FloatLayout:

        MDLabel:
            text: 'Facebook Reels Downloader'
            font_size: '25sp'
            bold : True
            halign: 'center'
            size: '400dp', '50dp'
            pos_hint: {'center_x': 0.5, 'top':1.4}

        MDTextField:
            id:url_input 
            hint_text: 'Reels URL'
            size_hint:.5,None
            pos_hint: {'center_x': 0.5, 'top':.6}
            icon_left : 'link'
            on_focus: app.Show_out(self) if self.focus else None

        MDRoundFlatIconButton:
            text: 'Download'
            icon: 'download'
            pos_hint: {'center_x': 0.5, 'top':.45}
            on_press:app.start_download()

        MDLabel:
            id : signal
            font_size: '15sp'
            halign: 'center'
            size_hint: None, None
            size: '400dp', '50dp'
            pos_hint: {'center_x': 0.5, 'top':.35}
            theme_text_color: 'Custom'
            text_color : 0,1,0,1

        MDLabel:
            text: 'Copy your Facebook Reel link, paste it into the input box, and click the Download button to enjoy a smooth, hassle-free downloading experience — completely free from annoying ads! [b]---- Developed by HRIDOY SHARMA[/b]'
            font_size: '15sp'
            halign: 'center'
            markup: True
            size: '400dp', '50dp'
            pos_hint: {'center_x': 0.5, 'top':1.2}

        MDLabel:
            text: "Dark Mode"
            id : mood
            halign: 'center'
            size: '400dp', '50dp'
            pos_hint: {'center_x': 0.9, 'top':1.45}

        MDSwitch:
            id: theme_switch
            active: False
            on_active: app.change_theme(self.active)
            pos_hint:{'center_x': 0.9,'center_y': 0.9}

        MDLabel:
            text: ""
            font_size: '15sp'
            pos_hint:{'center_x': 0.9,'center_y': 0.65}

        MDProgressBar:
            id: progress_bar
            value: 0
            max: 100
            color: 0, 1, 0, 1
            size_hint: .5, None
            height: '5dp'
            pos_hint: {'center_x': 0.5, 'top': .2}

        MDLabel:
            id: percentage
            text: '0%'
            halign: 'center'
            font_size: '13sp'
            size_hint: None, None
            size: '100dp', '30dp'
            pos_hint: {'center_x': 0.5, 'top': .28}
'''


class FDRDownloader(MDApp):
    def build(self):
        apps_body = Builder.load_string(kv)
        return apps_body

    def change_theme(self, theme):
        if theme:
            self.theme_cls.theme_style = 'Dark'
            self.root.md_bg_color = (0.08, 0.08, 0.08, 1)
            self.root.ids.mood.text = 'Light Mood'

        else:
            self.theme_cls.theme_style = 'Light'
            self.root.md_bg_color = (1, 1, 1, 1)
            self.root.ids.mood.text = 'Dark Mood'

    def start_download(self):
        url = self.root.ids.url_input.text.strip()
        try:
            file_manage = os.path.join(os.path.expanduser('~'), 'Downloads')
            options = {
                'format': 'best',
                'outtmpl': os.path.join(file_manage, '%(title)s.%(ext)s'),
            }
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])
                print('Download Successful')
                self.root.ids.url_input.text = ''
                self.root.ids.signal.text = 'Download Successful'
                self.root.ids.signal.text_color = 'green'
                self.root.ids.progress_bar.value = 100
                self.root.ids.percentage.text = '100%'

        except Exception as e:
            self.root.ids.signal.text = 'Download error. Try again.'
            self.root.ids.signal.text_color = 'red'
            self.root.ids.url_input.text = ''
            self.close_button = MDFlatButton(text='Close', on_release=self.Error_Handaling)
            self.error_some = MDDialog(
                title='Error',
                text='Something went wrong. Try again.',
                buttons=[self.close_button]
            )
            self.error_some.open()

        except NetworkError:
            net_close = MDFlatButton(text='Close', on_release=self.Error_Handaling)
            net_error = MDDialog(
                title='Network Error',
                text='Please check your internet connection.',
                buttons=[net_close]
            )
            net_error.open()

    def Error_Handaling(self, obj):
        self.error_some.dismiss()
        self.root.ids.progress_bar.value = 0
        self.root.ids.percentage.text = '0%'
        # Clock.schedule_once(lambda dt: setattr(self.root.ids.signal,'text',''),5)

    def Show_out(self, main):
        self.root.ids.signal.text = ''
        self.root.ids.progress_bar.value = 0
        self.root.ids.percentage.text = '0%'


if __name__ == '__main__':
    FDRDownloader().run()