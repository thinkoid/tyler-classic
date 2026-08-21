/* -*- mode: c; -*- */

#include <draw.h>
#include <font.h>
#include <malloc-wrapper.h>
#include <window.h>

struct draw_surface {
        Drawable drw;
        XftDraw *xft;
};

static struct rect *geometry_of(Drawable drw, struct rect *r)
{
        struct rect *pr = r;

        int x, y;
        unsigned w, h, bw, depth;

        Window ignore;

        if (0 == pr)
                pr = malloc_(sizeof *r);

        if (XGetGeometry(DPY, drw, &ignore, &x, &y, &w, &h, &bw, &depth)) {
                pr->x = x;
                pr->y = y;
                pr->w = w;
                pr->h = h;
        } else {
                if (pr != r) {
                        free(pr);
                        pr = 0;
                }
        }

        return pr;
}

struct draw_surface *make_draw_surface(int w, int h)
{
        struct draw_surface *p = malloc_(sizeof *p);
        memset(p, 0, sizeof *p);

        p->drw = XCreatePixmap(DPY, ROOT, w, h, DefaultDepth(DPY, SCRN));

        p->xft = XftDrawCreate(DPY, p->drw, VISUAL, COLORMAP);
        if (0 == p->xft) {
                fprintf(stderr, "XftDrawCreate failed");
                goto end;
        }

        return p;
end:
        XFreePixmap(DPY, p->drw);
        free(p);

        return 0;
}

void free_draw_surface(struct draw_surface *surf)
{
        XftDrawDestroy(surf->xft);
        XFreePixmap(DPY, surf->drw);
        free(surf);
}

void fill(struct draw_surface *surf, const struct rect *r, XftColor *bg)
{
        XSetForeground(DPY, GC_, bg->pixel);
        XFillRectangle(DPY, surf->drw, GC_, r->x, r->y, r->w, r->h);
}

void draw_text(struct draw_surface *surf, const char *s, int x, XftColor *fg,
               XftFont *fnt)
{
        int a, d, h, y;
        struct rect g = { 0 };

        if (0 == s || 0 == s[0])
                return;

        geometry_of(surf->drw, &g);
        ASSERT (g.x <= x && x < g.x + g.w);

        a = fnt->ascent;
        d = fnt->descent;
        h = a + d;

        y = g.y + (g.h / 2) - (h / 2) + a;

        XftDrawStringUtf8(surf->xft, fg, fnt, x, y, (XftChar8*)s, strlen(s));
}

void copy(struct draw_surface *surf,
          Drawable drw, int x, int y, int w, int h,
          int xto, int yto)
{
        XCopyArea(DPY, surf->drw, drw, GC_, x, y, w, h, xto, yto);
        XSync(DPY, 0);
}

