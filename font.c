/* -*- mode: c; -*- */

#include <font.h>
#include <display.h>

static XftFont *g_font /* = 0 */, *g_bold_font /* = 0 */;

XftFont *make_xftfont(Display *dpy, const char *s)
{
        XftFont *pf = XftFontOpenName(dpy, DefaultScreen(dpy), s);

        if (0 == pf) {
                fprintf(stderr, "cannot load font %s\n", s);
                exit(1);
        }

        return pf;
}

XftFont *make_font(const char *s)
{
        return (g_font = make_xftfont(DPY, s));
}

XftFont *make_bold_font(const char *s)
{
        return (g_bold_font = make_xftfont(DPY, s));
}

XftFont *font(void)
{
        return g_font;
}

XftFont *bold_font(void)
{
        return g_bold_font;
}

void free_font(void)
{
        XftFontClose(DPY, g_font);
        XftFontClose(DPY, g_bold_font);
        g_font = g_bold_font = 0;
}
