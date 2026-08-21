/* -*- mode: c; -*- */

#ifndef WM_FONT_H
#define WM_FONT_H

#include <defs.h>

#include <X11/Xft/Xft.h>
#include <fontconfig/fontconfig.h>

XftFont *font(void);
XftFont *bold_font(void);

XftFont *make_font(const char *);
XftFont *make_bold_font(const char *);

void free_font(void);

#define FNT (font())
#define FNT_BOLD (bold_font())

#endif /* WM_FONT_H */
