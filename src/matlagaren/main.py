import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib, Gdk, Gio
import gettext, locale, os, json, time, random
__version__ = "0.1.0"

APP_ID = "se.danielnylander.matlagaren"
LOCALE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'share', 'locale')
if not os.path.isdir(LOCALE_DIR): LOCALE_DIR = '/usr/share/locale'
try:
    locale.bindtextdomain(APP_ID, LOCALE_DIR)
    gettext.bindtextdomain(APP_ID, LOCALE_DIR)
    gettext.textdomain(APP_ID)
except Exception: pass
_ = gettext.gettext
def N_(s): return s

RECIPES = [
    {'name': N_('Sandwich'), 'icon': '🥪', 'steps': [N_('Get 2 slices of bread'), N_('Add butter'), N_('Add cheese'), N_('Add ham'), N_('Close sandwich'), N_('Cut in half'), N_('Done! Enjoy!')]},
    {'name': N_('Smoothie'), 'icon': '🥤', 'steps': [N_('Get a banana'), N_('Peel the banana'), N_('Put in blender'), N_('Add milk'), N_('Add berries'), N_('Blend!'), N_('Pour in glass')]},
    {'name': N_('Pancakes'), 'icon': '🥞', 'steps': [N_('Mix flour and milk'), N_('Add egg'), N_('Stir well'), N_('Heat the pan'), N_('Pour batter'), N_('Wait until bubbles'), N_('Flip!'), N_('Add toppings')]},
]

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title(_('Matlagaren'))
        self.set_default_size(500, 550)
        self._step = 0
        self._recipe = None

        header = Adw.HeaderBar()
        menu_btn = Gtk.MenuButton(icon_name='open-menu-symbolic')
        menu = Gio.Menu()
        menu.append(_('About'), 'app.about')
        menu_btn.set_menu_model(menu)
        header.pack_end(menu_btn)

        self._stack = Gtk.Stack()
        self._stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

        picker = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        picker.set_margin_top(24)
        picker.set_margin_start(24)
        picker.set_margin_end(24)
        title = Gtk.Label(label=_('What shall we make?'))
        title.add_css_class('title-2')
        picker.append(title)
        for i, r in enumerate(RECIPES):
            btn = Gtk.Button()
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            box.set_margin_top(8)
            box.set_margin_bottom(8)
            box.set_margin_start(12)
            box.set_margin_end(12)
            icon = Gtk.Label(label=r['icon'])
            icon.add_css_class('title-1')
            box.append(icon)
            name = Gtk.Label(label=_(r['name']))
            name.add_css_class('title-3')
            box.append(name)
            btn.set_child(box)
            btn.add_css_class('card')
            btn.connect('clicked', self._start, i)
            picker.append(btn)
        self._stack.add_titled(picker, 'picker', _('Recipes'))

        step_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        step_page.set_valign(Gtk.Align.CENTER)
        step_page.set_margin_top(32)
        step_page.set_margin_start(32)
        step_page.set_margin_end(32)
        self._s_icon = Gtk.Label()
        self._s_icon.add_css_class('title-1')
        step_page.append(self._s_icon)
        self._s_num = Gtk.Label()
        self._s_num.add_css_class('dim-label')
        step_page.append(self._s_num)
        self._s_text = Gtk.Label()
        self._s_text.add_css_class('title-2')
        self._s_text.set_wrap(True)
        step_page.append(self._s_text)
        self._s_prog = Gtk.ProgressBar()
        step_page.append(self._s_prog)
        done_btn = Gtk.Button(label=_('Done ✓'))
        done_btn.add_css_class('suggested-action')
        done_btn.add_css_class('pill')
        done_btn.connect('clicked', self._next)
        step_page.append(done_btn)
        back = Gtk.Button(label=_('← Back'))
        back.add_css_class('pill')
        back.connect('clicked', lambda b: self._stack.set_visible_child_name('picker'))
        step_page.append(back)
        self._stack.add_titled(step_page, 'steps', _('Steps'))

        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main.append(header)
        main.append(self._stack)
        self.set_content(main)

    def _start(self, btn, i):
        self._recipe = RECIPES[i]
        self._step = 0
        self._show_step()
        self._stack.set_visible_child_name('steps')

    def _show_step(self):
        r = self._recipe
        self._s_icon.set_text(r['icon'])
        self._s_num.set_text(_('Step %d of %d') % (self._step+1, len(r['steps'])))
        self._s_text.set_text(_(r['steps'][self._step]))
        self._s_prog.set_fraction((self._step+1)/len(r['steps']))

    def _next(self, btn):
        if self._step < len(self._recipe['steps'])-1:
            self._step += 1
            self._show_step()
        else:
            self._stack.set_visible_child_name('picker')

class App(Adw.Application):
    def __init__(self):
        super().__init__(application_id='se.danielnylander.matlagaren')
        self.connect('activate', lambda a: MainWindow(application=a).present())
        about = Gio.SimpleAction.new('about', None)
        about.connect('activate', lambda a,p: Adw.AboutDialog(application_name=_('Matlagaren'),
            application_icon=APP_ID, version=__version__, developer_name='Daniel Nylander',
            website='https://github.com/yeager/matlagaren', license_type=Gtk.License.GPL_3_0,
            comments=_('Step-by-step cooking')).present(self.get_active_window()))
        self.add_action(about)

def main(): App().run()
if __name__ == '__main__': main()

