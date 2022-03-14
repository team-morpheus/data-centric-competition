import os
import shutil
from typing import List

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.models.glyphs import ImageURL
from bokeh.plotting import figure, show


def _disable_all_for_pictures(p: figure) -> figure:  # pylint: disable=C0116
    p.toolbar.logo = None
    p.toolbar_location = None
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
    p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
    p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
    p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
    p.xaxis.major_label_text_font_size = "0pt"  # preferred method for removing tick labels
    p.yaxis.major_label_text_font_size = "0pt"  # preferred method for removing tick labels

    return p


def _save_tile_images_to_local_path(_photos_dir: str, max_photos: int) -> List[str]:  # pylint: disable=C0116
    # Save folders in curr folder for bokeh access
    os.makedirs("pics/", exist_ok=True)
    orig_img_paths = [os.path.join(_photos_dir, fname) for fname in os.listdir(_photos_dir)][:max_photos]
    copied_img_paths = [os.path.join("pics/", fname) for fname in os.listdir(_photos_dir)][:max_photos]
    for copied_im_p, orig_im_p in zip(copied_img_paths, orig_img_paths):
        shutil.copy(orig_im_p, copied_im_p)

    return copied_img_paths


def multi_channel_tile_slider(img_folder_path: str, max_photos: int = 100) -> None:
    """View interactively with bokeh the images."""
    c_img_paths = _save_tile_images_to_local_path(img_folder_path, max_photos)
    n = len(c_img_paths)

    # the plotting code
    plots = []
    sources = []
    plot_num = 1

    p = figure(height=300, width=300)
    # img_paths = paths[i]
    # print(img_paths)
    source = ColumnDataSource(
        data=dict(url=[c_img_paths[0]] * n, url_orig=c_img_paths, x=[1] * n, y=[1] * n, w=[1] * n, h=[1] * n)
    )
    image = ImageURL(url="url", x="x", y="y", w="w", h="h", anchor="bottom_left")
    p.add_glyph(source, glyph=image)
    _disable_all_for_pictures(p)

    plots.append(p)
    sources.append(source)

    update_source_str = """
        var data = source{i}.data;
        console.log(data);
        var url = data['url'];
        var url_orig = data['url_orig'];
        var i = 0;
        for (i = 0; i < url_orig.length; i++) {
            url[i] = url_orig[f-1]
        }
        source{i}.change.emit();

    """
    # the callback
    callback = CustomJS(
        args=dict(source0=sources[0]),
        code=f"""
        var f = cb_obj.value;
        console.log(f);
        {"".join([update_source_str.replace('{i}', str(i)) for i in range(plot_num)])}
    """,
    )
    slider = Slider(start=1, end=n, value=1, step=1, title="example number")
    slider.js_on_change("value", callback)

    column_layout = [slider]
    curr_row = []  # type: ignore
    for i in range(len(plots)):
        if i != 0 and i % 3 == 0:
            print(curr_row)
            column_layout.append(row(*curr_row.copy()))
            curr_row = []
        else:
            curr_row.append(plots[i])

    if len(curr_row) != 0:
        column_layout.append(row(*curr_row.copy()))

    layout = column(*column_layout)

    show(layout)
