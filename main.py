# for kivymd and md locals
import ast
import os
import webbrowser
from datetime import date
from typing import Union
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatIconButton, MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.pickers import MDColorPicker, MDTimePicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar


class StudyApp(MDApp):
    def __init__(self, bg_color):
        super().__init__()

        # locals layouts
        self.show_del_btn = False
        self.screen = None
        self.layout = None
        self.screen_manager = None
        self.main_layout = None

        # clr for background
        self.bg_color = bg_color

    def build(self):  # this is the main window of the App , has all widgets in this function.

        self.screen = MDScreen()
        self.screen.md_bg_color = self.bg_color
        self.screen.line_color = (0, 0, 0, 1)
        self.screen.line_width = 5
        self.screen.radius = 15

        self.layout = MDNavigationLayout()

        # Create a ScreenManager.
        self.screen_manager = ScreenManager()

        self.layout.add_widget(self.screen_manager)

        self.main_layout = MDBoxLayout(orientation="vertical", spacing=5,
                                       padding=5)  # main_layout for the main windows widgets.

        self.top_bar = MDTopAppBar(title="MyStudy", md_bg_color=(0.2, 0.5, 0.7, 1))
        self.top_bar.left_action_items = [["chevron-left", lambda x: self.Quit_Window("")]]
        self.top_bar.right_action_items = [["cog", lambda button: self.show_menu_settings(button, 'horizontal')]]
        self.top_bar.line_color = (0, 0, 0, 1)
        self.top_bar.specific_text_color = (0, 0, 0, 1)
        self.top_bar.radius = 5

        self.main_layout.add_widget(self.top_bar)

        self.header_layout = MDBoxLayout(orientation="horizontal", spacing=5, padding=5,
                                         size_hint=(1, 0.1))  # header_layout for the hears and other navigation's tools

        self.blinker_label = MDRaisedButton(text="Start Typer", halign="center", valign="center",
                                            theme_text_color="Custom", text_color="#8e24aaff",
                                            font_style="H5", on_press=self.start_typing, size_hint=(1, 1)
                                            )
        self.blinker_label.font_name = "NovaSquare-Regular.ttf"

        self.delete_btn = MDRectangleFlatIconButton(icon="delete", text="Delete : OFF", pos_hint={"center_y": 0.5},
                                                    theme_text_color="Custom", text_color=(0, 0.5, .5, 1),
                                                    line_color=(0, 0, 0, 1), icon_color=(0, 0, 1, 1),
                                                    on_release=self.Delete_Mode, md_bg_color=(1, 1, 1, 1),
                                                    size_hint=(1, 1))
        self.header_layout.add_widget(self.blinker_label)

        self.settings_menu = MDDropdownMenu(
            items=[
                {'text': 'Follow Me', 'viewclass': 'OneLineListItem',
                 'on_release': lambda x='Follow Me': self.show_settings(x)},
                {'text': 'Refresh', 'viewclass': 'OneLineListItem',
                 'on_release': lambda x='Refresh': self.show_settings(x)},
                {'text': 'Theme', 'viewclass': 'OneLineListItem',
                 'on_release': lambda x='Theme': self.show_settings(x)},
                {'text': 'Delete Student', 'viewclass': 'OneLineListItem',
                 'on_release': lambda x='Delete Student': self.show_settings(x)},
                {'text': 'About', 'viewclass': 'OneLineListItem',
                 'on_release': lambda x='About': self.show_settings(x)},
            ],
            width_mult=4,
        )  # this is a menu button items

        # header or nav bar widgets for top widgets placing

        self.main_layout.add_widget(self.header_layout)  # add the header layout to main_layout

        line = MDBoxLayout(size_hint=(1, 0.001), line_color=(0, 0, 0, 1), line_width=2.5)
        self.main_layout.add_widget(line)

        # The Users Lists
        self.scroll_view = MDScrollView()
        self.content_layout = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=10,
                                          md_bg_color=(0.7, 0.7, 0.7, 0.2), line_color=(0, 0, 0, 1),
                                          line_width=2.5)

        self.Upload_User_To_Window()
        # Add the grid layout to the scroll view
        self.scroll_view.add_widget(self.content_layout)

        # Create a grid layout to hold the widgets inside the scroll view
        # print(self.scroll_view.size_hint_x)

        self.main_layout.add_widget(self.scroll_view)
        # self.Upload_users_in_window()

        footer = MDLabel(text="Created by Valueia", font_style="H5", size_hint=(1, 0.1), pos_hint={"center_x": 0.5},
                         halign="center", theme_text_color="Custom", text_color=(0, 0.2, 0.7, 1))
        footer.font_name = "NovaSquare-Regular.ttf"

        self.main_layout.add_widget(footer)

        self.screen.add_widget(self.main_layout)
        self.screen.add_widget(self.layout)

        return self.screen

    def Quit_Window(self, instance):
        self.messagebox("Quit", "Do You Want To [b]Quit[/b]?", "[b][b][b]Yes[/b][/b][/b]")

    def Delete_Mode(self, instance):  # delete Mode is the mode to delete old or raw users.
        btn_bg_clr = instance.md_bg_color
        # print(btn_bg_clr)
        if btn_bg_clr == [1, 1, 1, 1]:
            instance.md_bg_color = (0.2, 1, 0.2, 1)
            instance.text = "Delete : ON"
            instance.text_color = (0, 0, 0, 1)
            toast("Delete Student Mode : ON")
        elif btn_bg_clr == [0.2, 1, 0.2, 1]:
            instance.md_bg_color = (1, 1, 1, 1)
            instance.text_color = (0, 0, 0, 1)
            instance.text = "Delete : OFF"
            toast("Delete Student Mode : OFF")

    def restart_window(
            self):  # restart the window using the self.content_layout, because the user who currently add in the file has not automatically uploaded in the Main window widgets, so, after click to reset the window is restart and the user widgets has been uploaded.
        self.content_layout.clear_widgets()
        self.Upload_User_To_Window()

    def close_popup(self, instance):  # close popup window
        self.popup_view.dismiss()

    def Create_User(self,
                    instance):  # main program to create user in the file : users.txt with student : name and class.
        if self.student_name.text != "" and self.student_class.text != "Class":
            file_layout = f"{self.student_name.text} - {self.student_class.text}"
            try:
                with open("Users.txt", "r") as r:
                    all_data = r.read().splitlines()
                    for user in all_data:
                        if user == file_layout:
                            toast(f"User Already Exist with {file_layout} Name!", duration=2)
                            break

                    else:
                        with open("Users.txt", "a") as file:
                            file.write("\n" + file_layout)
                        self.restart_window()
                        self.close_popup("")

                        toast(f"New Student {self.student_name.text} is Added!", duration=2)
            except FileNotFoundError:
                with open("Users.txt", "a") as a:
                    a.write("")




        else:
            toast("Please, Fill Entry to Add the Student.")

    def add_users(self, instance):  # pop up for the adding user in the file (pop up window)
        self.total_users = self.content_layout.children

        if len(self.total_users) != 11 and len(self.total_users) <= 11:

            # main window of popup by ModelView
            self.popup_view = ModalView(size_hint=(None, None), size=(800, 450))

            popup_content = MDBoxLayout(orientation="vertical", spacing=5, padding=5,
                                        md_bg_color=self.screen.md_bg_color)  # layout for widgets

            # header label
            header = MDLabel(text="~Enter Details~", halign="center",
                             font_style='H6', theme_text_color='Custom',
                             text_color=(0, 0, 0, 1), pos_hint={'center_y': 0.9},
                             font_name="NovaSquare-Regular.ttf"
                             )
            lbl = MDLabel(
                text="Enter the Some Details for Adding a New Student!",
                halign="center", theme_text_color="Custom",
                text_color=(0, 0.2, 0.7, 1))  # label for Something information

            self.student_name = MDTextField(hint_text="Name",
                                            text="",
                                            halign="left",
                                            size_hint=(0.5, 0.05),
                                            pos_hint={'center_x': 0.5},
                                            font_name="NovaSquare-Regular.ttf"
                                            )  # Nick Name Text Field
            # self.student_class = MDTextField(hint_text="Class",
            #                                  text="",
            #                                  halign="left",
            #                                  size_hint=(0.5, 0.05),
            #                                  pos_hint={'center_x': 0.5},
            #                                  font_name="NovaSquare-Regular.ttf"
            #                                  )  # host pin for connect to the HostApp-Server
            self.student_class = MDRaisedButton(text="Class", size_hint=(0.5, 0.1), halign="center",
                                                pos_hint={"center_x": 0.5},
                                                on_release=lambda button: self.show_menu_class(button, 'horizontal'))
            self.students_menu = MDDropdownMenu(
                items=[
                    {'text': '1 st', 'viewclass': 'OneLineListItem',
                     'on_release': lambda x='1 st': self.show_classes(x)},
                    {'text': '2 nd', 'viewclass': 'OneLineListItem',
                     'on_release': lambda x='2 nd': self.show_classes(x)},
                    {'text': '3 rd', 'viewclass': 'OneLineListItem',
                     'on_release': lambda x='3 rd': self.show_classes(x)},
                    {'text': '4 th', 'viewclass': 'OneLineListItem',
                     'on_release': lambda x='4 th': self.show_classes(x)},
                    {'text': '5 th', 'viewclass': 'OneLineListItem',
                     'on_release': lambda x='5 th': self.show_classes(x)},
                    {'text': '6 th', 'viewclass': 'OneLineListItem',
                     'on_release': lambda x='6 th': self.show_classes(x)},
                    {'text': '7 th', 'viewclass': 'OneLineListItem',
                     'on_release': lambda x='7 th': self.show_classes(x)},
                    {'text': '8 th', 'viewclass': 'OneLineListItem',
                     'on_release': lambda x='8 th': self.show_classes(x)},
                    {'text': '9 th', 'viewclass': 'OneLineListItem',
                     'on_release': lambda x='9 th': self.show_classes(x)},
                    {'text': '10 th', 'viewclass': 'OneLineListItem',
                     'on_release': lambda x='10 th': self.show_classes(x)},
                    {'text': '11 th', 'viewclass': 'OneLineListItem',
                     'on_release': lambda x='11 th': self.show_classes(x)},
                    {'text': '12 th', 'viewclass': 'OneLineListItem',
                     'on_release': lambda x='12 th': self.show_classes(x)},
                    {'text': 'up to 12 th', 'viewclass': 'OneLineListItem',
                     'on_release': lambda x='up to 12 th': self.show_classes(x)},
                ],
                width_mult=4,
            )  # this is a menu button items

            btn_lt = MDBoxLayout(orientation='horizontal', spacing=5,
                                 padding=15)  # btn_lt for add two buttons (cancel and connect).

            cancel = MDRectangleFlatIconButton(icon='close',
                                               text='Cancel',
                                               halign="center",
                                               size_hint=(1, 1),
                                               pos_hint={"center_x": 0.5},
                                               theme_text_color="Custom",
                                               line_color=(0, 0, 0, 0),
                                               on_release=self.close_popup)  # close for close popup window

            connect = MDRectangleFlatIconButton(icon='plus',
                                                text='Add',
                                                halign="center",
                                                size_hint=(1, 1),
                                                pos_hint={"center_x": 0.5},
                                                theme_text_color="Custom",
                                                line_color=(0, 0, 0, 0),
                                                on_release=self.Create_User
                                                )  # connect for connect to the Host and run Client App

            # add widgets to btn_lt (cancel, connect)
            btn_lt.add_widget(cancel)
            btn_lt.add_widget(connect)

            # add widgets to popup_content (header, lbl, nickname, host_pin, sn_host_pin, btn_lt)
            popup_content.add_widget(header)
            popup_content.add_widget(lbl)
            popup_content.add_widget(self.student_name)
            popup_content.add_widget(self.student_class)

            popup_content.add_widget(btn_lt)

            # add popup_content layout in popup_view
            self.popup_view.add_widget(popup_content)
            self.popup_view.open()  # open the popup view (popup window)
        else:
            # print("No space left!")
            toast("Only 10 Students Limit!")

    def show_menu_settings(self, button, menu_type):  # show the horizontal menu bar or drop down bar
        if menu_type == 'horizontal':

            self.settings_menu.caller = button
            self.settings_menu.open()
        else:
            pass

    def show_menu_class(self, button, menu_type):  # show the horizontal menu bar or drop down bar
        if menu_type == 'horizontal':

            self.students_menu.caller = button
            self.students_menu.open()
        else:
            pass

    def show_settings(self,
                      text):  # this is the menu options of the settings widget in the header_layout in main window.
        # print(f"Selected: {text}")
        if hasattr(self, "settings_menu"):
            # self.horizontal_menu.dismiss()
            if text == 'Follow Me':
                webbrowser.open_new_tab('https://www.youtube.com/@valuia')
            elif text == "Refresh":
                toast("Refreshed", duration=1)
                self.restart_window()
            elif text == "Theme":
                self.open_color_picker()
            elif text == "Delete Student":
                if self.show_del_btn == True:
                    self.show_del_btn = False
                elif self.show_del_btn == False:
                    self.show_del_btn = True

                if self.show_del_btn:
                    self.header_layout.remove_widget(self.blinker_label)
                    self.header_layout.add_widget(self.delete_btn)
                elif not self.show_del_btn:
                    self.header_layout.remove_widget(self.delete_btn)
                    self.header_layout.add_widget(self.blinker_label)

            elif text == "About":
                self.messagebox("About of The App",
                                "[b]Valīua Time Table App[/b]: Simplify scheduling, mark completed tasks. Efficient time management for enhanced productivity and organization.",
                                "Who is [b][b]Valueīa?[/b][/b]")
        else:
            pass
        self.settings_menu.dismiss()

    def show_classes(self, text):  # this is the menu options of the class of the student in the popup window.
        # print(f"Selected: {text}")
        if hasattr(self, "students_menu"):
            # self.horizontal_menu.dismiss()
            self.student_class.text = text
        self.students_menu.dismiss()

    def Upload_User_To_Window(self):  # placing the users name in the button widgets in the window
        try:

            # print(Clock.get_fps())

            with open("Users.txt", "r") as file:

                self.all_users = file.read().strip().split("\n")
                for i in self.all_users:
                    users = i
                    if users == "":
                        pass
                    else:
                        icn = "account"
                        btn = MDRectangleFlatIconButton(icon=icn, text=f"{users}",
                                                        pos_hint={"center_x": 0.5},
                                                        halign="center", size_hint=(0.5, 0.1), line_color=(0, 0, 0, 1),
                                                        line_width=1.5, on_release=self.Open_User_Data,
                                                        theme_text_color="Custom", text_color=(0, 0, 0, 1))
                        self.content_layout.add_widget(btn)
        except Exception as e:
            toast(str(e))

        add_btn = MDRaisedButton(text="--Add Another Student--", pos_hint={"center_x": 0.5},
                                 halign="center", size_hint=(0.5, 0.1), line_color=(0, 0, 0, 1),
                                 line_width=1.5, on_release=self.add_users,
                                 theme_text_color="Custom", text_color=(0, 0, 0, 1))
        self.content_layout.add_widget(add_btn)

    def Open_User_Data(self, instance):
        self.clicked_user = instance

        # In this Function We do Two Process 1st Open USer Data and 2nd Delete User if Delete Mode is On , else we only open the users Study Data.
        if self.delete_btn.md_bg_color == [0.2, 1, 0.2, 1]:
            # print("Deleting the user")
            self.messagebox("Delete Student", f"Do you want to [b]Delete[/b] the {self.clicked_user.text}?", "Yes")

            # self.Delete_Mode(instance)

        elif self.delete_btn.md_bg_color == [1, 1, 1, 1]:
            self.stop()
            UserStudyDataApp(self.clicked_user.text, self.screen.md_bg_color).run()

    def messagebox(self, title, text, cmd_btn_text):

        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRectangleFlatIconButton(
                    text="Cancel",
                    icon="close",
                    md_bg_color=(0.7, .2, 0, 1),
                    on_release=self.close_message_box),
                MDRectangleFlatIconButton(
                    text=cmd_btn_text,
                    icon="check",
                    md_bg_color=(0.2, 1, 0.2, 1),
                    on_release=self.process_action
                ),
            ],
        )
        self.dialog.open()

    def process_action(self, instance):  # call the self.Delete_clicked_user and dismiss the msg box

        if self.dialog.title == "Delete Student":
            self.Delete_clicked_Users(self.clicked_user)
        elif self.dialog.title == "Quit":
            self.stop()
        elif self.dialog.title == "About of The App":
            webbrowser.open_new_tab("https://www.instagram.com/aasan_kathat_1/")

        # Add your logic here
        self.dialog.dismiss()

    def close_message_box(self, instance):  # cose the messagebox
        # print(f"{instance} is not Deleted")
        toast("Canceled")

        self.dialog.dismiss()

    def Delete_clicked_Users(self, instance):  # delete the Clicked User.
        try:
            # Read the content of the file
            with open('Users.txt', 'r') as file:
                lines = file.readlines()

            filtered_lines = []
            for line in lines:
                if instance.text not in line:
                    filtered_lines.append(line)

            lines = filtered_lines

            # Write the updated content back to the file
            with open('Users.txt', 'w') as file:
                file.writelines(lines)
            # print(f"{instance} is Deleted")
            os.remove(f"Users_Time_Tables_{instance.text}.txt")
            os.remove(f"user_time_table_history_of_{instance.text}.txt")

            self.restart_window()
            toast(f"[Student: {instance.text}] is Deleted", duration=2)
        except Exception as e:
            toast(str(e))

    def open_color_picker(self):
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.open()
        color_picker.bind(
            on_select_color=self.on_select_color,
            on_release=self.get_selected_color,
        )

    def update_color(self, color: list) -> None:
        self.screen.md_bg_color = color

    def get_selected_color(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        '''Return selected color.'''

        #print(f"Selected color is {selected_color}")
        self.update_color(selected_color[:-1] + [1])

    def on_select_color(self, instance_gradient_tab, color: list) -> None:
        '''Called when a gradient image is clicked.'''

    def start_typing(self, instance):
        self.blinker_label.disabled = True
        self.text_list = [
            "Valīua Time Table App",
            "Created By Valuīa.",
            "Simplify scheduling.",
            "Mark completed tasks.",
            "With Valīua Time Table App", ''
        ]
        self.current_line = 0
        self.typed_text = ""
        self.current_index = 0
        self.is_typing_forward = True

        Clock.schedule_once(lambda dt: self.type_character(), 0)

    def type_character(self, dt=None):
        if 0 <= self.current_line < len(self.text_list):
            line = self.text_list[self.current_line]
            if self.current_line == 5:
                self.blinker_label.text = "Start Typer"
                self.blinker_label.disabled = False
            if 0 <= self.current_index < len(line):
                self.typed_text += line[self.current_index]
                self.blinker_label.text = f"{self.typed_text}|"
                self.current_index += 1
                Clock.schedule_once(lambda dt: self.type_character(), 0.1)
            elif self.is_typing_forward:
                self.is_typing_forward = False
                Clock.schedule_once(lambda dt: self.backspace_character(), 0.5)
            else:
                self.is_typing_forward = True
                self.current_line += 1
                self.current_index = 0
                Clock.schedule_once(lambda dt: self.type_character(), 1.0)

    def backspace_character(self, dt=None):
        if len(self.typed_text) > 0:
            self.typed_text = self.typed_text[:-1]
            self.blinker_label.text = f"{self.typed_text}|"
            Clock.schedule_once(lambda dt: self.backspace_character(), 0.1)
        else:
            Clock.schedule_once(lambda dt: self.type_character(), 1.0)


class UserStudyDataApp(MDApp):
    def __init__(self, student, bg_color):
        super().__init__()
        self.bg_color = bg_color
        self.student = student

    def build(self):
        self.screen = MDScreen()
        self.screen.md_bg_color = self.bg_color
        self.screen.line_color = (0, 0, 0, 1)
        self.screen.line_width = 5
        self.screen.radius = 15

        self.layout = MDNavigationLayout()

        # Create a ScreenManager
        self.screen_manager = ScreenManager()

        self.layout.add_widget(self.screen_manager)

        self.main_layout = MDBoxLayout(orientation="vertical", spacing=5,
                                       padding=5)  # main_layout for the main windows widgets.

        self.top_bar = MDTopAppBar(title=f"Student : {self.student}", md_bg_color=(0.2, 0.5, 0.7, 1))
        self.top_bar.left_action_items = [["chevron-left", lambda x: self.Quit_Window("")]]
        self.top_bar.right_action_items = [
            ["pencil", lambda x: self.edit_table()],
            ["history", lambda x: self.on_history()],
            ["check", lambda x: self.on_check()]
        ]

        self.top_bar.line_color = (0, 0, 0, 1)
        self.top_bar.specific_text_color = (0, 0, 0, 1)
        self.top_bar.radius = 5

        # Time Management Table
        self.data = {
            "header_row": ["Work", "Time"],
            "rows": []
        }

        rlst_data = self.read_schedule()  # this call is read the user time table data and return in a lst
        work, time = rlst_data[0], rlst_data[1]
        #print(rlst_data)
        try:
            for i in range(len(work)):
                self.data.get("rows").append([work[i], time[i]])
            #print(f"The Table is Completed : \n{self.data}")
        except Exception as e:
            toast(str(e))
        # Create table
        self.table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1, 1),
            use_pagination=False,
            column_data=[
                ("Work", dp(50)),
                ("Time", dp(50)),

            ],
            row_data=self.data["rows"],
            check=True,
            rows_num=len(self.data["rows"]),
            pagination_menu_height=dp(216),
        )
        self.table.padding = 10
        self.table.center = (0, 0)

        self.main_layout.add_widget(self.top_bar)
        self.main_layout.add_widget(self.table)

        self.screen.add_widget(self.layout)
        self.screen.add_widget(self.main_layout)
        return self.screen

    def edit_table(self):
        self.stop()
        EditTimeTableApp(self.bg_color, self.student).run()

    def on_check(self):
        # Handle check icon click
        #print("Check icon clicked")

        self.checked_work = self.table.get_row_checks()
        #print(self.checked_work)
        return self.Save_Today_Completed(self.checked_work)

    def Quit_Window(self, param):
        self.stop()
        StudyApp(self.bg_color).run()

    def read_schedule(self):
        try:
            with open(f"Users_Time_Tables_{self.student}.txt", "r") as r:
                fdata = r.read().strip().split(" - ")
                #print(fdata)

            work, time = fdata[0], fdata[1]
            #print(work, time)
            return self.str_to_lst(work, time)
        except FileNotFoundError:
            with open(f"Users_Time_Tables_{self.student}.txt", "w") as f:
                f.write(
                    "['work 1', 'work 2', 'work 3', 'work 4', 'work 5', 'work 6', 'work 7', 'work 8', 'work 9', 'work 10'] - ['Open Time Picker', 'Open Time Picker', 'Open Time Picker', 'Open Time Picker', 'Open Time Picker', 'Open Time Picker', 'Open Time Picker', 'Open Time Picker', 'Open Time Picker', 'Open Time Picker']")
            self.stop()
            EditTimeTableApp(self.bg_color, self.student).run()

    def str_to_lst(self, work, time):

        work_lst = ast.literal_eval(work)
        time_lst = ast.literal_eval(time)

        #print(work_lst, time_lst)

        return [work_lst, time_lst]

    def Save_Today_Completed(self, instance):
        checked_row = instance  # this is the Checked rows
        completed_data = {"work": [],
                          "time": []}  # the main dict for storing the work and time in the list.
        file_name = f"user_time_table_history_of_{self.student}.txt"  # the file name of the user history file
        if checked_row == []:  # if the checked row is blank , print please tick Your Completes
            toast("Please Tick Yours Completes.")  # toast for this info.
        else:  # otherwise continue
            for checked_line in checked_row:  # for loop - for give a line by line from the checked_row.
                #print("this line collected from the checked_rows: ", checked_line)
                work, time = checked_line[0], checked_line[1]  # checked line has two elements : 1. work , 2. time
                completed_data.get("work").append(work)  # adding the all works of checked_row
                completed_data.get("time").append(time)  # adding the all times of checked_row

                #print(completed_data)  # print the completed_data Dict

            today_date = date.today().strftime("%Y-%m-%d")  # contain the Today Date in today_date var.
            already_completed_data = []  # the list for we will add the already saved data in the future.
            try:
                with open(file_name, "r") as f:  # open the file as "f" name var
                    file_data = f.read()  # contain the file data in the file_data var.
                    #print(file_data)  # print the full file data
                    if today_date in file_data:  # check the today date is here in teh file data. if yes so >>>
                        lines = str(file_data).strip().split(
                            "\n")  # containing the all lines of file data in the "lines" list
                        for line in lines:  # put the line by line of the "lines" in "line".
                            #print(f"This is Collected line: {line}")  # print line
                            if today_date in line:  # check the : today date is here in the line , if true. so. >>>
                                #print(f"Yes, today date found in the {line}")  # print yes for data founded in the line
                                dt_data, work_data = line.strip().split(
                                    "~")  # the line contain the 3 var : 1. date , 2. work , 3. time
                                #print("\n yes, the date in this line: ", dt_data, " and the namaz in this line are: ",work_data, )  # print the date data , work data, time data
                                #print(completed_data)  # print the completed work and time
                                #print("the stored work = ", work_data)

                                # lst_data = self.str_to_lst(work=completed_data.get("work"), time=completed_data.get("time"))  # conv the
                                checked_data = [completed_data.get("work"), completed_data.get("time")]
                                stored_data = ast.literal_eval(work_data)

                                # for work_lst, time_lst in checked_data:
                                #     print(f"++ {work_lst} : {time_lst} ++")

                                #print(f"The checked_data : {checked_data}  |  The File Stored Data : {stored_data}")

                                # print(f"\n i am append the {work_lst} in the completed_namaz var : ", completed_data)
                                for c_work in checked_data[0]:
                                    #print(c_work)
                                    if c_work in stored_data:

                                        already_completed_data.append(c_work)
                                        #print(f"work is already completed! : {already_completed_data}")

                                    elif c_work not in stored_data:

                                        #print(f"the {c_work} not in the {dt_data} !")
                                        with open(file_name, "r") as f:
                                            past_data = f.read().split("\n")

                                            updated_past_data = past_data[0:len(past_data) - 1]
                                            #print(f"updated ::: {updated_past_data}")

                                        with open(file_name, "w") as wr:
                                            updated_file_str_data = ""
                                            for str_data in updated_past_data:
                                                if str_data != "":
                                                    updated_file_str_data += "\n" + str_data
                                            #print(f"str_ updated: {updated_file_str_data}")
                                            stored_data.append(c_work)
                                            wr.write(f"{updated_file_str_data}\n{today_date}~{stored_data}")
                                            toast(f"Works are Appended!", duration=3)
                        toast("Already Appended")


                    elif today_date not in file_data:

                        #print("today date not found in the file.")

                        with open(file_name, "a") as add:
                            layout = f"\n{today_date}~{completed_data.get('work')}"
                            add.write(layout)
                            toast(f"Works are Appended !")
                    else:
                        # toast("Somthing issue in these code !")
                        pass
            except FileNotFoundError:
                toast("Lets Try Again Now", duration=6)
                toast("    File Created    ", duration=4)
                toast("    Please Wait...    ", duration=2)
                with open(f"user_time_table_history_of_{self.student}.txt", "a") as f:
                    f.write("")

    def on_history(self):

        def close_popup(self):  # close window
            popup_view.dismiss()

        def btn_click(instance):
            date = str(instance.text).split("\n\n")
            toast(f"Created on {date[0]}.")

        # main widow ###################################################
        popup_view = ModalView(size_hint=(0.9725, 0.9))
        popup_content = MDBoxLayout(orientation="vertical", md_bg_color=self.bg_color)  # layout

        scroll_view = MDScrollView(size_hint=(1, 1))
        history_lt = MDBoxLayout(orientation="vertical", spacing=10, padding=5, adaptive_height=True)
        history_lt.md_bg_color = (1, 0.7, 0.7, 0.5)
        try:
            with open(f"user_time_table_history_of_{self.student}.txt", "r") as file:

                for line in file:

                    data = line.strip().split("~")
                    # print(data)
                    if data != [""]:
                        str_work = ""
                        date, str_lst = data[0], data[1]
                        work_lst = ast.literal_eval(str_lst)
                        for work in work_lst:
                            str_work += work + "\n"
                        #print(str_work)
                        data = date, str_work

                        updated_data = "\n\n".join(data)
                        btn = MDRaisedButton(text=f"{updated_data}", size_hint=(1, 0.1), on_release=btn_click)
                        history_lt.add_widget(btn)
        except Exception as e:
            toast(e)

        scroll_view.add_widget(history_lt)

        cancel_btn = MDRectangleFlatIconButton(icon='close',
                                               text='Cancel',
                                               pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                               size_hint=(0.5, 0.1),
                                               on_press=close_popup)

        # HEADER
        label = MDLabel(text="Your History", halign="center",
                        pos_hint={'center_x': 0.5, 'center_y': 1}, size_hint=(1, 0.2),
                        font_style='H6', theme_text_color='Custom', text_color=(.7, .7, .7, 1)
                        )
        popup_content.add_widget(label)
        popup_content.add_widget(scroll_view)
        popup_content.add_widget(cancel_btn)

        popup_view.add_widget(popup_content)
        popup_view.open()


class EditTimeTableApp(MDApp):
    def __init__(self, bg_color, student):
        super().__init__()
        self.bg_color = bg_color
        self.student = student
        self.work_info = []

    def build(self):
        self.screen = MDScreen()
        self.screen.md_bg_color = self.bg_color
        self.screen.line_color = (0, 0, 0, 1)
        self.screen.line_width = 5
        self.screen.radius = 15

        self.main_layout = MDBoxLayout(orientation="vertical", spacing=5,
                                       padding=5)  # main_layout for the main windows widgets.

        self.top_bar = MDTopAppBar(title=f"Edit Your Schedule Please", md_bg_color=(0.2, 0.5, 0.7, 1))
        self.top_bar.left_action_items = [["chevron-left", lambda x: self.Quit_Window()]]
        self.top_bar.right_action_items = [["check", lambda x: self.save_schedule(x)]]
        self.top_bar.line_color = (0, 0, 0, 1)
        self.top_bar.specific_text_color = (0, 0, 0, 1)
        self.top_bar.radius = 5

        self.scroll_view = MDScrollView()
        self.content_layout = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=100,
                                          md_bg_color=(0.7, 0.7, 0.7, 0.2), line_color=(0, 0, 0, 1),
                                          line_width=2.5)

        self.time_picker = MDTimePicker()

        rlst_data = self.read_schedule()
        #print(rlst_data)
        work, time = rlst_data
        try:

            for i in range(10):
                self.content_layout_contents_horizontal = MDBoxLayout(orientation="horizontal", spacing=10,
                                                                      adaptive_height=True)
                work_btn = MDTextField(icon_left="home", text=f"{work[i]}", hint_text=f"Work {i + 1}",
                                       pos_hint={"center_x": 0.5},
                                       size_hint=(0.5, 0.1),
                                       foreground_color=(0, 0, 0, 1))
                time_btn = MDRaisedButton(text=f"{time[i]}", on_release=self.show_time_picker)

                self.content_layout_contents_horizontal.add_widget(work_btn)
                self.content_layout_contents_horizontal.add_widget(time_btn)

                self.content_layout.add_widget(self.content_layout_contents_horizontal)
        except Exception as e:
            toast(str(e))

        # Add the grid layout to the scroll view
        self.scroll_view.add_widget(self.content_layout)

        self.main_layout.add_widget(self.top_bar)
        self.main_layout.add_widget(self.scroll_view)

        self.screen.add_widget(self.main_layout)

        return self.screen

    def show_time_picker(self, instance):
        self.clicked_btn = instance
        self.time_picker.bind(on_save=self.on_time_picker_save)
        self.time_picker.open()

    def on_time_picker_save(self, instance, time):
        #print(time)
        self.clicked_btn.text = f"Selected Time: {time.strftime('%H:%M')}"

    def Quit_Window(self):

        self.messagebox("Discard", "Do You Want to [b]Discard[/b]?", "[b]Discard[/b]")

    def save_schedule(self, x):
        yes = False
        self.work_info = {"work": [],
                          "time": []}
        full_list = []

        content_layout = self.root.children[0].children[0].children[0]
        #print(content_layout.md_bg_color)
        #print(content_layout.children)

        for widgets in content_layout.children:
            for widgets_all in widgets.children:
                full_list.append(widgets_all.text)

        full_list.reverse()
        #print(full_list)

        time_list = []
        work_list = []

        for i in full_list:
            if yes == True:
                time_list.append(i)
                yes = False
            elif yes == False:
                work_list.append(i)
                yes = True
        #print(f"this is work list : {work_list}")
        #print(f"this is time list : {time_list}")

        for k in range(10):

            str(f"{work_list[k]} : {time_list[k]}")
        self.work_info.get("work").append(work_list)
        self.work_info.get("time").append(time_list)

        #print(self.work_info)
        with open(f"Users_Time_Tables_{self.student}.txt", "w") as file:
            file.write(f'{self.work_info.get("work")[0]} - {self.work_info.get("time")[0]}')

        self.stop()
        UserStudyDataApp(self.student, self.bg_color).run()
        toast("Saved", duration=1)

        # self.read_schedule()

    def read_schedule(self):

        with open(f"Users_Time_Tables_{self.student}.txt", "r") as r:
            fdata = r.read().splitlines()
            for line in fdata:
                work, time = line.split(" - ")
                # for work, time in raw_data.:

                return self.str_to_lst(work, time)

    def str_to_lst(self, work, time):

        work_lst = ast.literal_eval(work)
        time_lst = ast.literal_eval(time)

        #print(work_lst, time_lst)

        return [work_lst, time_lst]

    def messagebox(self, title, text, cmd_btn_text):

        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRectangleFlatIconButton(
                    text="Cancel",
                    icon="close",
                    md_bg_color=(0.7, .2, 0, 1),
                    theme_text_color="Custom",
                    text_color=(0, 0, 0, 1),
                    icon_color=(1, 0.09, 0.2, 1),
                    on_release=self.close_message_box),
                MDRectangleFlatIconButton(
                    text=cmd_btn_text,
                    icon="check",
                    md_bg_color=(0.2, 1, 0.2, 1),
                    theme_text_color="Custom",
                    text_color=(0, 0, 0, 1),
                    on_release=self.process_action
                ),
            ],
        )
        self.dialog.open()

    def process_action(self, instance):  # call the self.Delete_clicked_user and dismiss the msg box

        if self.dialog.title == "Discard":
            # os.remove(f"Users_Time_Tables_{self.student}.txt")
            toast("File [b]Discard[/b]")
            self.stop()
            StudyApp(self.bg_color).run()

        # Add your logic here
        self.dialog.dismiss()

    def close_message_box(self, instance):  # cose the messagebox
        # print(f"{instance} is not Deleted")
        toast("Canceled")

        self.dialog.dismiss()


if __name__ == '__main__':
    StudyApp((0.8, 0.8, 0.8, 1)).run()
