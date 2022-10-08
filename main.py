from kivy.app import App
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.lang import Builder
from kivy.uix.bubble import Bubble
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.config import Config
import subprocess
import shutil
import os

# cool yellow color IDK if I will use #fcba03

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
kv = Builder.load_file("screen.kv")


class CreateScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(CreateScreen, self).__init__(**kwargs)
        self.canvas.add(Color(40 / 255, 40 / 255, 38 / 255))
        self.canvas.add(RoundedRectangle(pos=(250, 150), size=(320, 350)))

    def add_widget(self, widget):
        super(CreateScreen, self).add_widget(widget)


class BuilderGui(App):
    def build(self):
        # Main GUI Window
        Window.clearcolor = ("#333230")
        self.window = CreateScreen(size=(300, 300))
        self.window.size_hint = (.5, .5)
        self.window.add_widget(
            Label(text='Create New Plugin', font_size="30sp", color="#a6a095", pos=(210, 320), bold=True))
        self.username = TextInput(multiline=False, background_color="#2e2d2b", cursor_color="#a6a095",
                                  foreground_color="#a6a095", size_hint=(.47, .1), pos=(360, 350))
        self.plugin_name = TextInput(multiline=False, background_color="#2e2d2b", cursor_color="#a6a095",
                                     foreground_color="#a6a095", size_hint=(.47, .1), pos=(360, 300))
        self.window.add_widget(self.username)
        self.window.add_widget(self.plugin_name)
        self.window.add_widget(Label(text='Username', font_size="17sp", color="#a6a095", pos=(100, 215), bold=True))
        self.window.add_widget(Label(text='Plugin Name', font_size="17sp", color="#a6a095", pos=(105, 167), bold=True))
        self.button = Button(text="Create", background_normal="", background_color="#1c1c1b", color="#a6a095",
                             size_hint=(.3, .1), pos=(430, 170))
        self.button.bind(on_press=self.plugin_create)
        self.window.add_widget(self.button)
        self.back_button = Button(text="Back", background_normal="", background_color="#1c1c1b", color="#a6a095",
                                  size_hint=(.3, .1), pos=(280, 170))
        self.back_button.bind(on_press=self.back)
        self.window.add_widget(self.back_button)
        self.info_text = Label(text='All fields must be filled', font_size="17sp", color="#a61919", pos=(205, 120),
                               bold=True)

        return self.window

    def back(self, instance):
        print("Back")

    def plugin_create(self, instance):
        self.fields = 0
        # Check to make sure all the fields are filled
        if self.username.text == "" or self.plugin_name.text == "":
            self.window.add_widget(self.info_text)
        else:
            self.window.remove_widget(self.info_text)
            self.fields += 1

        if self.fields == 1:
            # Empty's Project directory
            try:
                shutil.rmtree("Project")
            except:
                pass

            # Copys gradle files to Project directory
            shutil.copytree("Gradle", "Project")

            # creates the main file structure
            os.makedirs(
                "Project/src/main/java/" + self.username.text + "/src/com/" + self.username.text + "/" + self.plugin_name.text)
            os.makedirs("Project/src/main/resources")

            # Code to generate the Main plugin java class
            f = open(
                "Project/src/main/java/" + self.username.text + "/src/com/" + self.username.text + "/" + self.plugin_name.text + "/Main.java",
                "a")
            text = open("Files/main.txt")
            f.write("package com." + self.username.text + "." + self.plugin_name.text + ";\n")
            for line in text:
                f.write(line)
            text.close()
            f.close()

            # Code to create the plugin.yml
            f = open("Project/src/main/resources/plugin.yml", "a")
            f.write("author: " + self.username.text + "\n")
            f.write("version: 1.0\n")
            f.write("api-version: 1.19\n")
            f.write("name: " + self.plugin_name.text.lower() + "\n")
            f.write("main: com." + self.username.text + "." + self.plugin_name.text + ".Main")
            f.close()

            # Adds the neccesary text to build.gradle that includes all the dependencies
            f = open("Project/build.gradle", "a")
            text = open("Files/gradle_build.txt")
            for line in text:
                f.write(line + "\n")
            f.close()
            text.close()

            # Creates the gradle_build.bat
            path = os.path.abspath("Project/gradlew.bat")
            build_bat = open("Project/gradle_build.bat", "a")
            build_bat.write("@echo off\n")
            build_bat.write("gradlew.bat build")
            build_bat.close()

            # Changes working directory to Project directory
            mydir = os.getcwd()  # would be the MAIN folder
            mydir_tmp = mydir + "/Project"  # add the testA folder name
            mydir_new = os.chdir(mydir_tmp)  # change the current working directory

            # Gets the path and runs the gradle_build.bat
            path = os.path.dirname(os.path.realpath("Project"))
            p = subprocess.Popen(["gradle_build.bat"], shell=True, cwd=path)
            stdout, stderr = p.communicate()

            os.rename("build/libs/Gen-1.0-SNAPSHOT.jar", "build/libs/" + self.plugin_name.text + ".jar")

            print("Finished making plugin")


if __name__ == "__main__":
    BuilderGui().run()
