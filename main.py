from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDTextButton, MDFlatButton, MDFloatingActionButton
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField, MDTextFieldRect

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.relativelayout import RelativeLayout
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

import datetime
import os


class Card(MDCard):
    def __init__(self, title="Title", desc="Description", day="", month="", year="", note_num=0, content=None,
                 file_present=False, **kwargs):
        super().__init__(**kwargs)
        self.card_layout = RelativeLayout(size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
        self.elevation = 1
        self.radius = [1, 1, 1, 1]
        self.height = Window.height/5.5
        self.size_hint_y = None
        self.year = year
        self.day = day
        self.month = month
        self.title = title
        self.description = desc
        self.content = content
        self.file_present = file_present
        self.note_num = note_num
        self.add_widgets()
        self.add_menu()
        self.set_delete_confirmation_dialog()
        self.set_edit_dialog()
        self.note_file_name = self.title
        self.create_file()
        if file_present:
            self.note_file_name = self.title
            self.screen_name = self.note_file_name

        self.screen_created = False

    def edit_file_properties(self, title, desc, date):
        self.content_text = self.screen.note_part.text
        with open(f"Note Files/{self.note_file_name}.txt", "w") as f:
            f.writelines(f"{title}\n")
            f.writelines(f"{desc}\n")
            f.writelines(f"{date}\n")
            f.writelines("\n")
            f.close()

        with open(f"Note Files/{self.note_file_name}.txt", "a") as f:
            f.write(self.content_text)
            f.close()

    def create_file(self):
        if not self.file_present:
            self.screen_name = self.note_file_name

            self.screen = NoteScreen(name=self.screen_name, note=self.content)  # Create screen if no file is present
            App.screen_manager.add_widget(self.screen)
            self.screen_created = True

            with open(f"Note Files/{self.note_file_name}.txt", "w") as f:
                f.writelines(f"{self.title}\n")
                f.writelines(f"{self.description}\n")
                f.writelines(f"{self.day}/{self.month}/{self.year}\n")
                f.writelines("\n")
                f.close()

    def set_edit_dialog(self):
        dialog_contents = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            size_hint_y=None,
        )
        self._title_field = MDTextField(
            hint_text="Title",
            helper_text="Required (can only have numbers or text)",
            helper_text_mode="on_error",
            error=False,
            text=self.title,
            size_hint_y=None,
            height=dp(25),
            size_hint_x=1,
            text_color_focus="black",
            text_color_normal="black"
        )
        self._description_field = MDTextField(
            hint_text="Description",
            multiline=False,
            text=self.description,
            size_hint_y=None,
            height=dp(50),
            size_hint_x=1,
            text_color_focus="black",
            text_color_normal="black"
        )
        date_layout = GridLayout(
            rows=1,
            cols=4,
            size_hint_x=1,
            spacing=dp(5),
            size_hint_y=None
        )

        self._day_field =  MDTextField(
            hint_text = "Day",
            text=self.day,
            size_hint = (None, None),
            size_hint_x=1 / 4,
            text_color_focus= "black",
            text_color_normal = "black",
            input_filter="int"
        )
        self._month_field = MDTextField(
            hint_text = "Month",
            text=self.month,
            size_hint = (None, None),
            size_hint_x=1 / 4,
            text_color_focus="black",
            text_color_normal="black",
            input_filter="int"
        )
        self._year_field = MDTextField(
            helper_text = "Write full year",
            helper_text_mode="on_error",
            hint_text="Year",
            text = self.year,
            size_hint = (None, None),
            size_hint_x=1/4,
            text_color_focus="black",
            text_color_normal="black",
            input_filter="int"
        )
        calender_icon = MDIconButton(icon="calendar-month",
                                    on_release=self.show_date_picker)


        date_layout.add_widget(self._day_field)
        date_layout.add_widget(self._month_field)
        date_layout.add_widget(self._year_field)
        date_layout.add_widget(calender_icon)

        dialog_contents.add_widget(self._title_field)
        dialog_contents.add_widget(self._description_field)
        dialog_contents.add_widget(date_layout)

        dialog_contents.height = date_layout.height + self._title_field.height + self._description_field.height + dp(15)

        self.edit_dialog = MDDialog(
            title="Edit contents",
            type="custom",
            content_cls=dialog_contents,
            buttons=[MDFlatButton(
                text = "Cancel",
                on_release = self.close_edit_dialog
                                ),
                    MDFlatButton(
                        text = "Save",
                        on_release = self.confirm_edit
                                )
            ]
        )
    def open_edit_menu(self, instance):
        self._title_field.helper_text = "Required (can only have numbers or text)"
        self.edit_dialog.open()

    def close_edit_dialog(self, instance):
        self.edit_dialog.dismiss()

    def title_only_has_spaces(self, txt):
        return txt.strip() == ''

    def title_has_non_alpha_numeric(self, txt):
        if self.title_only_has_spaces(txt):
            return False
        for char in txt:
            if not (char.isalnum() or char.isspace()):
                return True
        return False

    def confirm_edit(self, instance):
        any_error = False

        day = self._day_field.text
        month = self._month_field.text
        year = self._year_field.text


        if len(day) > 2 or len(day) < 1:
            self._day_field.error = True
            any_error = True
        else:
            if int(day) <= 0 or int(day) > 31:
                self._day_field.error = True
                any_error = True


        if len(month) == 0 or len(month) > 2:
            self._month_field.error = True
            any_error = True
        else:
            if int(month) <= 0 or int(month) > 12:
                self._month_field.error = True
                any_error = True

        if len(year) == 0:
            self._year_field.error = True
            any_error = True
        else:
            if len(year) != 4 or int(year) <= 0:
                self._year_field.error = True
                any_error = True

        if (self._title_field.text in App.home_screen.note_titles) and (self.title != self._title_field.text):
            self._title_field.error = True
            self._title_field.helper_text = "Use an unique title"
            any_error = True
        elif self._title_field.text not in App.home_screen.note_titles:
            if len(self._title_field.text) == 0:
                self._title_field.error = True
                any_error = True
            elif self.title_has_non_alpha_numeric(self._title_field.text) == True:
                self._title_field.error = True
                any_error = True

        if any_error == True:
            any_error = False
        else:

            self.title_label.text = self._title_field.text
            self.description_label.text = self._description_field.text
            self.title = self._title_field.text
            self.description = self._description_field.text

            if len(day) == 1:
                day = f"0{day}"
            if len(month) == 1:
                month = f"0{month}"

            self.day = day
            self.month = month
            self.year = year
            self.date_label.text = f"Date: {day}/{month}/{year}"
            self.edit_file_properties(title=self.title_label.text, desc=self.description_label.text, date=f"{day}/{month}/{year}")
            App.home_screen.note_titles.remove(self.note_file_name)
            App.home_screen.note_titles.append(self.title)
            self.rename_file(self.title)
            self.edit_dialog.dismiss()
            self.menu.dismiss()

    def rename_file(self, new_name):
        os.rename(f"Note Files/{self.note_file_name}.txt", f"Note Files/{self.title}.txt")
        self.note_file_name = self.title

    def set_delete_confirmation_dialog(self):
        self.delete_dialog = MDDialog(
            title = "Delete this note?",
            text = "It cannot be recovered after deletion",
            buttons=[
                MDFlatButton(text="Cancel", on_press=self.close_delete_conf_dialog),
                MDFlatButton(text="Confirm", on_press=self.delete_itself)
            ]
        )

    def open_delete_conf_dialog(self, instance):
        self.delete_dialog.open()
    def close_delete_conf_dialog(self, instance):
        self.delete_dialog.dismiss()
    def add_menu(self):
        self.menu_items = [
            {
                "viewclass": "MDFlatButton",
                "text": "Edit",
                "on_release": lambda x="Item1": self.open_edit_menu(x)

            },
            {
                "viewclass": "MDFlatButton",
                "text": "Delete",
                "on_release": lambda x="Item2": self.open_delete_conf_dialog(x)

            }
        ]
        self.menu = MDDropdownMenu(items=self.menu_items, caller=self.menu_button)

    def open_menu(self, instance):
        self.menu.open()
    def show_date_picker(self, picker):
        self.date_dialog.open()
        self.date_dialog.size_hint_x = None

    def delete_itself(self, x):
        self.menu.dismiss()
        self.delete_dialog.dismiss()
        os.remove(f"Note Files/{self.note_file_name}.txt")
        App.home_screen.note_titles.remove(self.note_file_name)
        App.home_screen.delete_item(self)

    def date_picker_save(self, instance, value, date_range):
        _value = str(value)
        self.year = _value[0:4]
        self.month = _value[5:7]
        self.day = _value[8:10]

        self._day_field.text = self.day
        self._month_field.text = self.month
        self._year_field.text = self.year

    def create_screen(self, name):
        screen_name = name
        self.screen = NoteScreen(name=screen_name, note=self.content)
        App.screen_manager.add_widget(self.screen)

        # Fix = Create screen only after enter button is pressed

    def go_to_screen(self, instance):
        if not App.screen_manager.has_screen(self.screen_name):
            self.create_screen(self.screen_name)
            self.screen_created = True
        self.screen.set_file_name(self.note_file_name)
        App.screen_manager.transition.direction = "left"
        App.screen_manager.current = self.screen_name

    def add_widgets(self):
        self.menu_button = MDIconButton(pos_hint={"top": 1, "right": 1},
                                                 icon="dots-vertical", on_release=self.open_menu)

        self.edit_content_button = MDIconButton(pos_hint={"right": 1, "y": 0}, icon="notebook-edit-outline",
                                                on_release=self.go_to_screen)
        self.card_layout.add_widget(self.menu_button)
        self.card_layout.add_widget(self.edit_content_button)

        self.date_dialog = MDDatePicker(input_field_text_color_normal="white", helper_text = "")

        self.date_dialog.bind(on_save=self.date_picker_save)
        self.date_label = MDTextButton(text="Date", pos_hint={"x": 0.02, "top": 0.95},
                                       size_hint = (None, None), valign="top", halign="left",
                                       disabled=True)

        self.title_label = MDLabel(pos_hint={"x": 0.02, "center_y": 0.5}, text=self.title, valign="middle",
                                   halign="left", font_style="Body1")
        self.description_label = MDLabel(text=self.description, pos_hint={"x": 0.02, "y": 0.15},
                                size_hint_y = None, valign="bottom", halign="left",
                                              disabled_color="black", height=self.minimum_height,
                                                width=self.minimum_width, padding=[0, 0, dp(50), dp(10)],
                                               font_style="Caption")

        self.card_layout.add_widget(self.title_label)
        self.card_layout.add_widget(self.date_label)
        self.card_layout.add_widget(self.description_label)
        self.add_widget(self.card_layout)
        self.date_label.text = f"Date: {self.day}/{self.month}/{self.year}"

    def save_note(self, note):
        pass

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.no_of_files = 0

        self.file_path_list = []

        self.full_time = datetime.datetime.now()
        self.note_titles = []

        self.day = self.full_time.strftime("%d")
        self.month = self.full_time.strftime("%m")
        self.year = self.full_time.strftime("%Y")
        self.opened_app = False

    def on_enter(self):

        if not self.opened_app:
            float_layout = FloatLayout()

            scroll_view = ScrollView(size_hint=(1, 1), pos_hint={"top": 1})

            self.main_layout = GridLayout(
                cols=1, size_hint_y=None, padding=[dp(10), dp(5), dp(10), 0], spacing=dp(5)
            )
            scroll_view.add_widget(self.main_layout)
            float_layout.add_widget(scroll_view)
            float_layout.add_widget(MDFloatingActionButton(
                icon="plus", pos_hint={"right": 0.95, "y": 0.03}, on_release=self.open_dialog
            ))

            self.add_widget(float_layout)

            self.create_dialog()
            self.create_date_dialog()
            self.create_note_list()
            self.opened_app = True

    def create_note_list(self):
        for filename in os.scandir("Note Files"):
            if filename.is_file():
                self.no_of_files += 1
                self.file_path_list.append(filename.path)

        for i, filepath in enumerate(self.file_path_list):
            with open(filepath, "r") as f:
                file_content = f.read()
                lines = file_content.split("\n")
                title = lines[0]
                self.note_titles.append(title)
                desc = lines[1]
                date = lines[2]
                day=date[0:2]
                month=date[3:5]
                year=date[6:10]
                content = lines[4::]
                new_note = Card(title=title, desc=desc, day=day, month=month, year=year, note_num=int(i)+1,
                                content=content, file_present=True)
                self.main_layout.add_widget(new_note)
                f.close()


    def create_date_dialog(self):
        self.date_dialog = MDDatePicker(input_field_text_color_normal="white", helper_text="")
        self.date_dialog.bind(on_save=self.date_picker_save)
    def create_dialog(self):
        dialog_contents = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            size_hint_y=None,
        )
        self.title_field = MDTextField(
            hint_text="Title",
            helper_text="Required (can only have numbers or text)",
            helper_text_mode="on_error",
            error=False,
            size_hint_y=None,
            height=dp(25),
            size_hint_x=1,
            text_color_focus="black",
            text_color_normal="black"
        )
        self.description_field = MDTextField(
            hint_text="Description",
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            size_hint_x=1,
            text_color_focus="black",
            text_color_normal="black"
        )
        date_layout = GridLayout(
            rows=1,
            cols=4,
            size_hint_x=1,
            spacing=dp(5),
            size_hint_y=None
        )

        self.day_field = MDTextField(
            hint_text="Day",
            text=self.day,
            size_hint=(None, None),
            size_hint_x=1 / 4,
            text_color_focus="black",
            text_color_normal="black",
            input_filter="int"
        )
        self.month_field = MDTextField(
            hint_text="Month",
            text=self.month,
            helper_text_mode="on_error",
            size_hint=(None, None),
            size_hint_x=1 / 4,
            text_color_focus="black",
            text_color_normal="black",
            input_filter="int"
        )
        self.year_field = MDTextField(
            helper_text="Write full year",
            helper_text_mode="on_error",
            hint_text="Year",
            text=self.year,
            size_hint=(None, None),
            size_hint_x=1 / 4,
            text_color_focus="black",
            text_color_normal="black",
            input_filter="int"
        )
        calender_icon = MDIconButton(icon="calendar-month",
                                     on_release=self.show_date_picker)

        date_layout.add_widget(self.day_field)
        date_layout.add_widget(self.month_field)
        date_layout.add_widget(self.year_field)
        date_layout.add_widget(calender_icon)

        dialog_contents.add_widget(self.title_field)
        dialog_contents.add_widget(self.description_field)
        dialog_contents.add_widget(date_layout)

        dialog_contents.height = date_layout.height + self.title_field.height + self.description_field.height + dp(15)

        self.new_item_dialog = MDDialog(
            title="Make new note",
            type="custom",
            content_cls=dialog_contents,
            buttons=[MDFlatButton(
                text="Cancel",
                on_release=self.close_dialog
            ),
                MDFlatButton(
                    text="Save",
                    on_release=self.add_item

                )
            ]
        )

    def date_picker_save(self, instance, value, date_range):
        _value = str(value)
        self.year = _value[0:4]
        self.month = _value[5:7]
        self.day = _value[8:10]

        self.day_field.text = self.day
        self.month_field.text = self.month
        self.year_field.text = self.year

    def show_date_picker(self, instance):
        self.date_dialog.open()

    def close_dialog(self, instance):
        self.new_item_dialog.dismiss()
        self.day_field.text = self.day
        self.month_field.text = self.month
        self.year_field.text = self.year
        self.title_field.text = ""
        self.description_field.text = ""

    def open_dialog(self, instance):
        self.new_item_dialog.open()

    def delete_item(self, item):
        self.main_layout.remove_widget(item)

    def title_only_has_spaces(self, txt):
        return txt.strip() == ''
    def title_has_non_alpha_numeric(self, txt):
        if self.title_only_has_spaces(txt):
            return False
        for char in txt:
            if not (char.isalnum() or char.isspace()):
                return True
        return False

    def add_item(self, instance):
        self.title_field.helper_text = "Required (can only have numbers or text)"
        any_error = False
        if self.title_field.text in App.home_screen.note_titles:
            self.title_field.error = True
            self.title_field.helper_text = "Use an unique title"
            any_error = True
        elif self.title_field.text not in App.home_screen.note_titles:
            if len(self.title_field.text) == 0:
                self.title_field.error = True
                any_error = True
            elif self.title_has_non_alpha_numeric(self.title_field.text) == True:
                self.title_field.error = True
                any_error = True

        if len(self.year_field.text) == 0:
            self.year_field.error = True
            any_error = True
        else:
            if len(self.year_field.text) != 4 or int(self.year_field.text) <= 0:
                self.year_field.error = True
                any_error = True

        if len(self.month_field.text) == 0 or len(self.month_field.text) > 2:
            self.month_field.error = True
            any_error = True
        else:
            if int(self.month_field.text) <= 0 or int(self.month_field.text) > 12:
                self.month_field.error = True
                any_error = True
        if len(self.day_field.text) > 2 or len(self.day_field.text) < 1:
            self.day_field.error = True
            any_error = True
        else:
            if int(self.day_field.text) <= 0 or int(self.day_field.text) > 31:
                self.day_field.error = True
                any_error = True

        if any_error == True:
            any_error = False
        else:
            self.no_of_files += 1
            new_note = Card(title=self.title_field.text, day=self.day_field.text, month=self.month_field.text,
                            desc=self.description_field.text, year=self.year_field.text,
                            note_num=self.no_of_files)
            self.main_layout.add_widget(new_note)
            self.note_titles.append(self.title_field.text)
            self.close_dialog(None)


class NoteScreen(MDScreen):
    def __init__(self, note="", **kwargs):
        super().__init__(**kwargs)
        self.note = note
        self.file_name = ""
        self.entered_once = False


        # Display part:
        float_layout = FloatLayout()
        box_layout = BoxLayout(orientation="vertical")
        top_bar = MDTopAppBar(
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[["content-save", lambda x: self.save_note()]]
        )
        self.note_part = MDTextFieldRect()
        box_layout.add_widget(top_bar)
        box_layout.add_widget(self.note_part)
        float_layout.add_widget(box_layout)

        self.add_widget(float_layout)
    def set_file_name(self, name):
        self.file_name = name
    def on_enter(self):
        if not self.entered_once:
            if self.note is not None:
                for line in self.note:
                    self.note_part.text += line + "\n"
                self.entered_once = True
# Write everything in python file. Dont use KV
    def save_note(self, dt=None):
        note = self.note_part.text
        with open(f"Note Files/{self.file_name}.txt", 'r') as f:
            file_content = f.read()
            lines = file_content.split("\n")
            title = lines[0]
            desc = lines[1]
            date = lines[2]
            content = self.note_part.text
            f.close()
        with open(f"Note Files/{self.file_name}.txt", 'w') as f:
            f.writelines(f"{title}\n")
            f.writelines(f"{desc}\n")
            f.writelines(f"{date}\n")
            f.writelines("\n")
            f.close()
        with open(f"Note Files/{self.file_name}.txt", 'a') as f:
            f.write(content)
            f.close()

    def go_back(self):
        self.save_note()
        App.screen_manager.transition.direction = "right"
        App.screen_manager.current = "home_screen"

class CustomScreenManager(ScreenManager):
    def has_screen(self, name):
        return name in self.screen_names

class JournalApp(MDApp):
    def build(self):
        self.create_folder()
        Window.size= (315, 700)
        self.height = Window.height
        self.width = Window.width
        self.theme_cls.theme_style = "Light"
        self.home_screen = HomeScreen(name="home_screen")
        self.screen_manager = CustomScreenManager()
        self.screen_manager.add_widget(self.home_screen)
        self.screen_manager.current = "home_screen"
        return self.screen_manager

    def create_folder(self):
        if not os.path.exists("Note Files"):
            os.mkdir("Note Files")

if __name__ == "__main__":
    App = JournalApp()
    App.run()