import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gdk
import threading
import os
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk4agg import FigureCanvas
from vocal_analyzer import VocalAnalyzer
import json
import urllib.request

class VocalPulseApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.sarath.vocalpulse',
                         flags=gi.repository.Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        self.win = Adw.ApplicationWindow(application=self, title="VocalPulse - Studio Comparison")
        self.win.set_default_size(900, 700)

        # Main Layout
        main_layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.win.set_content(main_layout)

        # Header bar (Persistent)
        header = Adw.HeaderBar()
        main_layout.append(header)

        # Tab Switching (ViewStack)
        self.view_stack = Adw.ViewStack()
        self.view_stack.set_vexpand(True)
        main_layout.append(self.view_stack)

        # Tab Switcher in Header
        switcher = Adw.ViewSwitcher(stack=self.view_stack)
        header.set_title_widget(switcher)

        # 1. Analyzer Page
        analyzer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        analyzer_box.set_margin_top(30)
        analyzer_box.set_margin_bottom(30)
        analyzer_box.set_margin_start(30)
        analyzer_box.set_margin_end(30)
        self.view_stack.add_titled(analyzer_box, "analyzer", "Analyze")

        # Video Info Container
        self.video_info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.title_label = Gtk.Label(label="Select a recording to begin")
        self.title_label.set_max_width_chars(50)
        self.title_label.set_ellipsize(3) # Pango.EllipsizeMode.END
        self.title_label.set_selectable(True)
        self.title_label.add_css_class("video-title")
        
        # Right-click to copy (GTK4 Gestures)
        right_click = Gtk.GestureClick(button=Gdk.BUTTON_SECONDARY)
        right_click.connect("pressed", self.on_title_right_click)
        self.title_label.add_controller(right_click)
        
        self.video_info.append(self.title_label)
        analyzer_box.append(self.video_info)

        # 2. History Page
        self.history_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.history_box.set_margin_top(30)
        self.history_box.set_margin_bottom(30)
        self.history_box.set_margin_start(30)
        self.history_box.set_margin_end(30)
        self.view_stack.add_titled(self.history_box, "history", "History")

        # --- Analyzer Page Content ---
        # --- Analysis Bar (The "One-Row" Design) ---
        analysis_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        analysis_bar.add_css_class("card")
        analysis_bar.set_margin_top(15)
        analysis_bar.set_margin_bottom(15)
        analysis_bar.set_margin_start(15)
        analysis_bar.set_margin_end(15)
        analyzer_box.append(analysis_bar)

        # 1. File Upload
        file_btn = Gtk.Button(label="📁 Select Vocal Recording")
        file_btn.connect("clicked", self.on_select_file)
        analysis_bar.append(file_btn)
        
        self.selected_file_path = None
        self.file_label = Gtk.Label(label="No file selected", xalign=0)
        self.file_label.set_hexpand(True)
        analysis_bar.append(self.file_label)

        # 2. YouTube Link & Search
        self.link_entry = Gtk.Entry(placeholder_text="Song name or YouTube Link...")
        self.link_entry.set_hexpand(True)
        analysis_bar.append(self.link_entry)

        search_btn = Gtk.Button(label="🔍 Search")
        search_btn.connect("clicked", self.on_search_clicked)
        analysis_bar.append(search_btn)

        # Reset Button
        reset_btn = Gtk.Button(label="🔄 Reset")
        reset_btn.connect("clicked", self.on_reset_fields)
        analysis_bar.append(reset_btn)

        # 3. Analyze & Stop Buttons
        self.analyze_button = Gtk.Button(label="Analyze")
        self.analyze_button.add_css_class("suggested-action")
        self.analyze_button.connect("clicked", self.on_analyze_clicked)
        analysis_bar.append(self.analyze_button)

        self.stop_button = Gtk.Button(label="Stop")
        self.stop_button.add_css_class("destructive-action")
        self.stop_button.set_sensitive(False)
        self.stop_button.connect("clicked", self.on_stop_clicked)
        analysis_bar.append(self.stop_button)

        # Progress Bar
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_visible(False)
        self.progress_bar.set_margin_top(10)
        self.progress_bar.set_margin_bottom(10)
        analyzer_box.append(self.progress_bar)
        self.pulse_id = 0

        # --- Result Section ---
        result_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        analyzer_box.append(result_box)

        self.rating_label = Gtk.Label(label="-- / 100")
        self.rating_label.add_css_class("title-1")
        self.rating_label.add_css_class("rating-display")
        result_box.append(self.rating_label)

        self.feedback_label = Gtk.Label(label="Ready to compare your vocals with the original track.")
        self.feedback_label.add_css_class("body")
        result_box.append(self.feedback_label)

        # --- Charts ---
        chart_frame = Gtk.Frame()
        chart_frame.set_vexpand(True)
        result_box.append(chart_frame)

        self.fig = Figure(figsize=(8, 6), facecolor='#1e1e1e')
        self.ax_pitch = self.fig.add_subplot(111)
        self.ax_pitch.set_facecolor('#1e1e1e')
        for spine in self.ax_pitch.spines.values(): spine.set_color('#444444')
        self.ax_pitch.tick_params(colors='white')
        self.ax_pitch.set_title("Vocal Pitch Comparison", color='white')

        self.canvas = FigureCanvas(self.fig)
        chart_frame.set_child(self.canvas)

        style_provider = Gtk.CssProvider()
        style_provider.load_from_path('style.css')
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.build_history_view()
        self.analyzer = VocalAnalyzer() 
        self.thumb_cache = os.path.expanduser("~/.local/share/vocalpulse/cache/thumbnails")
        os.makedirs(self.thumb_cache, exist_ok=True)
        self.win.present()
        self.is_running = False
        self.current_proc = None
        
        # Setup Search Completion
        self.search_store = Gtk.ListStore(str)
        self.completion = Gtk.EntryCompletion()
        self.completion.set_model(self.search_store)
        self.completion.set_text_column(0)
        self.link_entry.set_completion(self.completion)
        self.load_search_history()

    def build_history_view(self):
        title = Gtk.Label(label="Your Vocal History")
        title.add_css_class("title-1")
        self.history_box.append(title)

        # Scrolled Window for Table
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        self.history_box.append(scrolled)

        # Modern GTK4 ListBox for better performance
        self.history_list = Gtk.ListBox()
        self.history_list.set_selection_mode(Gtk.SelectionMode.NONE)
        self.history_list.add_css_class("card")
        
        viewport = Gtk.Viewport()
        viewport.set_child(self.history_list)
        scrolled.set_child(viewport)
        
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.history_box.append(btn_box)
        
        refresh_btn = Gtk.Button(label="Refresh History")
        refresh_btn.connect("clicked", lambda x: self.refresh_history())
        btn_box.append(refresh_btn)

        clear_btn = Gtk.Button(label="🗑️ Clear All History")
        clear_btn.connect("clicked", self.on_clear_history_clicked)
        btn_box.append(clear_btn)
        
        self.refresh_history()

    def refresh_history(self):
        # Clear ListBox properly
        while (child := self.history_list.get_first_child()):
            self.history_list.remove(child)
            
        history_path = os.path.expanduser("~/.local/share/vocalpulse/history.json")
        if os.path.exists(history_path):
            try:
                with open(history_path, "r") as f:
                    history = json.load(f)
                    for entry in reversed(history):
                        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
                        row.set_margin_top(10)
                        row.set_margin_bottom(10)
                        row.set_margin_start(15)
                        row.set_margin_end(15)
                        
                        date_lbl = Gtk.Label(label=entry.get("timestamp", ""))
                        date_lbl.add_css_class("dim-label")
                        
                        song_lbl = Gtk.Label(label=entry.get("song_title", "Unknown"))
                        song_lbl.set_hexpand(True)
                        song_lbl.set_halign(Gtk.Align.START)
                        song_lbl.set_ellipsize(3) # Pango.EllipsizeMode.END
                        
                        score_lbl = Gtk.Label(label=f"{entry.get('score', 0):.1f}/100")
                        score_lbl.add_css_class("accent-label")
                        
                        row.append(date_lbl)
                        row.append(song_lbl)
                        row.append(score_lbl)
                        self.history_list.append(row)
            except Exception as e:
                print(f"Error reading history: {e}")

    def on_search_clicked(self, btn):
        query = self.link_entry.get_text()
        if not query:
            self.feedback_label.set_text("Enter a song name to search!")
            return
        
        self.feedback_label.set_text("Searching YouTube...")
        self.progress_bar.set_visible(True)
        self.progress_bar.pulse()
        
        def do_search():
            results = self.analyzer.search_youtube(query)
            GLib.idle_add(self.show_search_results, results)
            
        threading.Thread(target=do_search, daemon=True).start()

    def show_search_results(self, results):
        self.progress_bar.set_visible(False)
        if not results:
            self.feedback_label.set_text("No results found.")
            return
            
        popover = Gtk.Popover()
        popover.set_parent(self.link_entry)
        popover.set_autohide(True)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(15)
        main_box.set_margin_bottom(15)
        main_box.set_margin_start(15)
        main_box.set_margin_end(15)
        popover.set_child(main_box)
        
        label = Gtk.Label(label="Top Search Results")
        label.add_css_class("title-4")
        main_box.append(label)
        
        for res in results:
            # Result Card
            card = Gtk.Button()
            card.add_css_class("flat")
            card.connect("clicked", self.on_result_selected, res['url'], popover)
            
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
            card.set_child(hbox)
            
            # Thumbnail Container
            thumb_container = Gtk.Box()
            thumb_container.set_size_request(120, 68) # 16:9 ratio
            thumb_container.add_css_class("thumbnail-container")
            hbox.append(thumb_container)
            
            image = Gtk.Image()
            image.set_pixel_size(120)
            thumb_container.append(image)
            
            # Text Info
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            vbox.set_valign(Gtk.Align.CENTER)
            hbox.append(vbox)
            
            title_lbl = Gtk.Label(label=res['title'])
            title_lbl.set_wrap(True)
            title_lbl.set_max_width_chars(40)
            title_lbl.set_xalign(0)
            title_lbl.add_css_class("heading")
            vbox.append(title_lbl)
            
            dur_lbl = Gtk.Label(label=f"⏱ {res['duration']}")
            dur_lbl.set_xalign(0)
            dur_lbl.add_css_class("caption")
            vbox.append(dur_lbl)
            
            # Right-click to copy from search results
            result_right_click = Gtk.GestureClick(button=Gdk.BUTTON_SECONDARY)
            result_right_click.connect("pressed", lambda g, n, x, y, u=res['url']: self.on_search_right_click(g, n, x, y, u, card))
            card.add_controller(result_right_click)
            
            main_box.append(card)
            
            # Download thumbnail in background
            threading.Thread(target=self.load_thumbnail, args=(res['thumbnail'], res['id'], image), daemon=True).start()
            
        popover.popup()

    def on_search_right_click(self, gesture, n_press, x, y, url, parent_widget):
        menu = Gtk.PopoverMenu()
        menu.set_parent(parent_widget)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        box.set_margin_top(5); box.set_margin_bottom(5)
        box.set_margin_start(5); box.set_margin_end(5)
        
        copy_btn = Gtk.Button(label="📋 Copy Link")
        copy_btn.connect("clicked", lambda x: self.copy_to_clipboard(url, menu))
        box.append(copy_btn)
        
        menu.set_child(box)
        menu.popup()

    def load_thumbnail(self, url, video_id, gtk_image):
        local_path = os.path.join(self.thumb_cache, f"{video_id}.jpg")
        try:
            if not os.path.exists(local_path):
                urllib.request.urlretrieve(url, local_path)
            
            GLib.idle_add(self.set_image_from_path, gtk_image, local_path)
        except Exception as e:
            print(f"Failed to load thumbnail: {e}")

    def set_image_from_path(self, gtk_image, path):
        try:
            # In GTK4, we can use Gdk.Texture.new_from_filename
            texture = Gdk.Texture.new_from_filename(path)
            gtk_image.set_from_paintable(texture)
        except Exception as e:
            print(f"Error setting image: {e}")

    def on_result_selected(self, btn, url, popover):
        self.link_entry.set_text(url)
        self.current_ref_url = url
        popover.popdown()
        self.feedback_label.set_text("Song selected. Ready to Analyze!")

    def on_title_right_click(self, gesture, n_press, x, y):
        url = getattr(self, 'current_ref_url', None)
        if not url: return
        
        menu = Gtk.PopoverMenu()
        menu.set_parent(self.title_label)
        
        # Simple box for the menu content
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        box.set_margin_top(5)
        box.set_margin_bottom(5)
        box.set_margin_start(5)
        box.set_margin_end(5)
        
        copy_btn = Gtk.Button(label="📋 Copy YouTube Link")
        copy_btn.connect("clicked", lambda x: self.copy_to_clipboard(url, menu))
        box.append(copy_btn)
        
        menu.set_child(box)
        menu.popup()

    def copy_to_clipboard(self, text, popover):
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set(text)
        popover.popdown()
        self.feedback_label.set_text("Link copied to clipboard! ✅")

    def on_select_file(self, btn):
        dialog = Gtk.FileDialog(title="Open Vocal File")
        filter_audio = Gtk.FileFilter()
        filter_audio.set_name("Audio Files")
        filter_audio.add_mime_type("audio/*")
        filters = gi.repository.Gio.ListStore.new(Gtk.FileFilter)
        filters.append(filter_audio)
        dialog.set_filters(filters)

        dialog.open(self.win, None, self.on_file_dialog_response)

    def on_file_dialog_response(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            if file:
                self.selected_file_path = file.get_path()
                self.file_label.set_text(os.path.basename(self.selected_file_path))
        except Exception as e:
            print(f"Error opening file: {e}")

    def on_analyze_clicked(self, btn):
        if not self.selected_file_path:
            self.feedback_label.set_text("Please select a vocal file first!")
            return
        
        youtube_link = self.link_entry.get_text().strip()
        if not youtube_link:
            self.feedback_label.set_text("Please paste a YouTube link for comparison!")
            return

        self.progress_bar.set_visible(True)
        self.feedback_label.set_text("Downloading and Isolating vocals with AI... (this may take a minute)")
        
        # Start Progress Pulse Timer
        if self.pulse_id == 0:
            self.pulse_id = GLib.timeout_add(100, self.do_pulse)
        
        self.is_running = True
        GLib.idle_add(self.stop_button.set_sensitive, True)
        GLib.idle_add(self.analyze_button.set_sensitive, False)
        
        self.analysis_thread = threading.Thread(target=self.run_analysis, args=(youtube_link, None))
        self.analysis_thread.daemon = True
        self.analysis_thread.start()

    def on_stop_clicked(self, button):
        self.is_running = False
        # Hard kill the current subprocess
        if hasattr(self.analyzer, 'current_proc') and self.analyzer.current_proc:
            try:
                self.analyzer.current_proc.terminate()
                print("🛑 Terminated active forensic process.")
            except: pass
            
        GLib.idle_add(self.feedback_label.set_text, "🛑 Analysis Stopped by User")
        GLib.idle_add(self.stop_button.set_sensitive, False)
        GLib.idle_add(self.analyze_button.set_sensitive, True)
        GLib.idle_add(self.progress_bar.set_fraction, 0.0)

    def do_pulse(self):
        if self.progress_bar.get_visible():
            self.progress_bar.pulse()
            return True
        self.pulse_id = 0
        return False

    def run_analysis(self, youtube_link, song_title):
        try:
            if not self.is_running: return
            self.analyzer.file_path = self.selected_file_path
            self.analyzer.load_audio()
            
            # Phase 1: Fetch and Sync Music
            GLib.idle_add(self.feedback_label.set_text, "Phase 1: Syncing Background Music DNA...")
            ref_f0, song_title = self.analyzer.fetch_reference(youtube_link)
            
            if not self.is_running: return
            if ref_f0 is None:
                GLib.idle_add(self.feedback_label.set_text, "Error: Failed to fetch reference track.")
                return

            # Phase 2: Verify Identity
            GLib.idle_add(self.feedback_label.set_text, f"Phase 2: Verifying Identity for {song_title}...")
            fingerprint, linearity, is_passed = self.analyzer.verify_identity(self.analyzer.ref_full_y)
            
            if not self.is_running: return
            if not is_passed:
                feedback = (
                    f"❌ Error: Not the same song! (Mismatch detected)\n"
                    f"Acoustic DNA Match: {fingerprint*100:.1f}% (Need >75%)\n"
                    f"Sync Linearity: {linearity*100:.1f}% (Target: >40%)"
                )
                GLib.idle_add(self.update_ui, 0.0, feedback, np.zeros(10), np.zeros(10, dtype=bool), None, youtube_link, song_title)
                return

            # Phase 3: High-Precision Vocal Analysis
            GLib.idle_add(self.feedback_label.set_text, "Phase 3: Performing High-Precision Vocal Analysis...")
            self.analyzer.analyze_pitch(quick=False)
            rating, feedback = self.analyzer.calculate_rating(reference_f0=ref_f0)

            if not self.is_running: return
            GLib.idle_add(self.update_ui, rating, feedback, self.analyzer.f0, self.analyzer.voiced_flag, self.analyzer.ref_f0, youtube_link, song_title)
        except Exception as e:
            GLib.idle_add(self.feedback_label.set_text, f"❌ Error: {str(e)}")
        finally:
            self.is_running = False
            GLib.idle_add(self.stop_button.set_sensitive, False)
            GLib.idle_add(self.analyze_button.set_sensitive, True)

    def update_ui(self, rating, feedback, f0, voiced, ref_f0=None, youtube_link=None, song_title=None):
        self.rating_label.set_text(f"{rating:.1f} / 100")
        self.feedback_label.set_text(feedback)
        self.progress_bar.set_visible(False)
        
        if song_title and song_title != "Unknown":
            self.link_entry.set_text(song_title)
            
        self.save_search_history(youtube_link)
        self.save_history(rating, feedback, youtube_link, song_title)
        self.refresh_history()

        # Plot
        self.ax_pitch.clear()
        times = np.arange(len(f0)) * (512 / 22050)
        
        # Downsample
        step = max(1, len(f0) // 1000)
        times_ds = times[::step]
        f0_ds = f0[::step]
        voiced_ds = voiced[::step]
        
        # Plot Studio Reference (Dimmed Red)
        if ref_f0 is not None:
            ref_times = np.arange(len(ref_f0)) * (512 / 22050)
            ref_step = max(1, len(ref_f0) // 1000)
            self.ax_pitch.plot(ref_times[::ref_step], ref_f0[::ref_step], color='#ff4b2b', marker='.', markersize=2, linestyle='None', alpha=0.5, label="Studio Track")
        
        # Plot User Vocals (Bright Cyan)
        if np.any(voiced_ds):
            self.ax_pitch.plot(times_ds[voiced_ds], f0_ds[voiced_ds], color='#00f2fe', marker='o', markersize=1, linestyle='None', label="Your Vocals")
        else:
            self.ax_pitch.plot(times_ds, f0_ds, color='#444444', alpha=0.3)
            
        self.ax_pitch.set_title("Vocal Pitch Comparison (Red: Studio | Cyan: You)")
        self.ax_pitch.grid(True, color='#333333', alpha=0.3)
        self.ax_pitch.legend(loc='upper right', facecolor='#1e1e1e', labelcolor='white')
        
        # Draw on idle to ensure thread safety
        GLib.idle_add(self.canvas.draw)

    def save_history(self, rating, feedback, youtube_link, song_title):
        if rating <= 0: return # ONLY save real songs that passed the matching gate
        
        import json
        from datetime import datetime
        history_file = os.path.expanduser("~/.local/share/vocalpulse/history.json")
        self.is_running = False
        self.analysis_thread = None
        history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, "r") as f:
                    history = json.load(f)
            except:
                pass
        
        # Human readable timestamp
        time_str = datetime.now().strftime("%H:%M | %d %b")
        
        entry = {
            "timestamp": time_str,
            "vocal_file": self.selected_file_path if hasattr(self, 'selected_file_path') else "None",
            "youtube_link": youtube_link,
            "song_title": song_title if song_title and song_title != "Unknown" else "Performance",
            "score": rating,
            "feedback": feedback
        }
        history.append(entry)
        try:
            with open(history_file, "w") as f:
                json.dump(history, f, indent=4)
        except Exception as e:
            print(f"Failed to save history: {e}")

    def on_reset_fields(self, btn):
        self.on_stop_clicked(None)
        self.link_entry.set_text("")
        self.selected_file_path = None
        self.file_label.set_text("No file selected")
        self.rating_label.set_text("-- / 100")
        self.feedback_label.set_text("Ready for new forensic recording. ✨")
        self.progress_bar.set_visible(False)
        self.progress_bar.set_fraction(0.0)
        
        try:
            self.ax_pitch.clear()
            self.ax_pitch.set_facecolor('#111111')
            self.ax_pitch.set_title("Vocal Pitch Comparison", color='white', fontsize=12, pad=15)
            self.ax_pitch.set_xlabel("Time (seconds)", color='#888888')
            self.ax_pitch.set_ylabel("Pitch (Hz)", color='#888888')
            self.canvas.draw()
        except: pass

    def on_clear_history_clicked(self, btn):
        history_path = os.path.expanduser("~/.local/share/vocalpulse/history.json")
        if os.path.exists(history_path):
            os.remove(history_path)
        self.refresh_history()
        self.feedback_label.set_text("All history cleared!")

    def load_search_history(self):
        history_file = os.path.expanduser("~/.local/share/vocalpulse/search_history.json")
        if os.path.exists(history_file):
            try:
                with open(history_file, "r") as f:
                    searches = json.load(f)
                    for s in searches:
                        self.search_store.append([s])
            except: pass

    def save_search_history(self, search_term):
        if not search_term or len(search_term) < 10: return
        history_file = os.path.expanduser("~/.local/share/vocalpulse/search_history.json")
        searches = []
        if os.path.exists(history_file):
            try:
                with open(history_file, "r") as f:
                    searches = json.load(f)
            except: pass
        if search_term not in searches:
            searches.insert(0, search_term)
            searches = searches[:30] # Keep last 30
            with open(history_file, "w") as f:
                json.dump(searches, f)
            self.search_store.insert(0, [search_term])

if __name__ == '__main__':
    app = VocalPulseApp()
    app.run(None)
