import os
from typing import List

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.models.glyphs import ImageURL
from bokeh.plotting import figure, show
from tqdm import trange


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


def _save_tile_images_to_local_path(_photos_dir: str, max_photos: int = 1000) -> List[str]:  # pylint: disable=C0116
    # Save folders in curr folder for bokeh access
    os.makedirs("pics/", exist_ok=True)
    a_img_paths = []
    for i in trange(min(4, max_photos), desc="loading tiles"):
        # img_a = None[i][0][0]  # noqa

        a_img_p = f"pics/{i}-A.png"

        # def save_to_png(img_channel, p):
        #     data = np.random.randint(5, size=(224, 224), dtype=np.uint8)
        #
        #     data[...] = img_channel.numpy() * 255
        #     # rgbArray[..., 0] = img_channel.numpy() * 255
        #     # rgbArray[..., 2] = img_channel.numpy() * 255
        #     Image.fromarray(data).save(p)
        #
        # save_to_png(img_a_p, a_img_p)  # noqa

        a_img_paths.append(a_img_p)

    return a_img_paths


def multi_channel_tile_slider() -> None:
    """View interactively with bokeh the 3 image tiles."""
    n = 2
    # a_img_paths, b_img_paths, c_img_paths = _save_tile_images_to_local_path(dataset, n)

    img_paths_orig = [
        "pics\\1-A.png",
        "pics\\2-A.png",
    ]

    # the plotting code
    plots = []
    sources = []
    paths = [img_paths_orig, img_paths_orig, img_paths_orig]
    plot_num = 3

    for i in range(plot_num):
        p = figure(height=300, width=300)
        img_paths = paths[i]
        # print(img_paths)
        source = ColumnDataSource(
            data=dict(url=[img_paths_orig[0]] * n, url_orig=img_paths, x=[1] * n, y=[1] * n, w=[1] * n, h=[1] * n)
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
        args=dict(source0=sources[0], source1=sources[1], source2=sources[2]),
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
