import sublime
import sublime_plugin

import os

from .PrettyJson import PrettyJsonBaseCommand

s = sublime.load_settings("Pretty JSON.sublime-settings")


def is_sublime_file(view: sublime.View) -> bool:
  if not view.file_name():
      return False
  
  extension = os.path.splitext(view.file_name())[1]
  return extension.startswith('.sublime-')


class PrettyJsonLintListener(sublime_plugin.EventListener, PrettyJsonBaseCommand):
    def on_post_save(self, view):
        if not s.get("validate_on_save", True):
            return
        self.view = view

        as_json = s.get("as_json", ["JSON"])
        if any(syntax in view.settings().get("syntax") for syntax in as_json) and not is_sublime_file(view):
            self.clear_phantoms()
            json_content = view.substr(sublime.Region(0, view.size()))
            try:
                self.json_loads(json_content)
            except Exception as ex:
                region = sublime.Region(0, view.size())
                self.show_exception(region=region, msg=ex)


class PrettyJsonAutoPrettyOnSaveListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if not s.get("pretty_on_save", False):
            return
        self.view = view

        as_json = s.get("as_json", ["JSON"])
        if any(syntax in view.settings().get("syntax") for syntax in as_json) and not is_sublime_file(view):
            view.run_command("pretty_json")
