/* -*- mode: c; -*- */

#ifndef WM_DRAWABLE_H
#define WM_DRAWABLE_H

#include <defs.h>
#include <display.h>
#include <geometry.h>

#include <X11/Xlib.h>
#include <X11/Xft/Xft.h>

struct draw_surface;

struct draw_surface *make_draw_surface(int width, int height);
struct draw_surface *draw_surface(void);

void free_draw_surface(struct draw_surface *surf);

void fill(struct draw_surface * surf,
          const struct rect *r, XftColor *bg);

void draw_text(struct draw_surface *surf,
               const char *s, int x, XftColor *fg, XftFont *fnt);

void copy(struct draw_surface *surf,
          Drawable drw, int x, int y, int w, int h,
          int xto, int yto);

#endif /* WM_DRAWABLE_H */
