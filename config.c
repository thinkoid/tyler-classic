/* -*- mode: c; -*- */

#include <defs.h>
#include <config.h>

/* clang-format off */
static int g_showbar      =  1;
static int g_border_width =  1;

static int   g_master_size  = 1;
static float g_master_ratio = .5f;

static size_t g_margin = 2;

static const char *g_fontname = "Iosevka Light:size=12";

static const char *g_colors[] = {
        "#444444", "#222222", "#BBBBBB", "#93a660", "#8c9440", "#EEEEEE"
};

static const int g_cursors[] = {
        XC_top_left_arrow, XC_sizing, XC_fleur
};

static const char *g_termcmd[] = {
        "st", 0
};

/* import(1) has no shell of its own; the date stamp needs one. */
static const char *g_screenshotcmd[] = {
        "sh", "-c",
        "import -window root "
        "\"$HOME/Pictures/screenshot-$(date +%Y%m%d-%H%M%S).png\"",
        0
};

static int g_snap = 5;
/* clang-format on */

const char *config_fontname(void)
{
        return g_fontname;
}

const char **config_colors(void)
{
        return g_colors;
}

size_t config_margin(void)
{
        return g_margin;
}

size_t config_colors_size(void)
{
        return SIZEOF(g_colors);
}

const int *config_cursors(void)
{
        return g_cursors;
}

size_t config_cursors_size(void)
{
        return SIZEOF(g_cursors);
}

const char **config_termcmd(void)
{
        return g_termcmd;
}

const char **config_screenshotcmd(void)
{
        return g_screenshotcmd;
}

int config_showbar(void)
{
        return g_showbar;
}

int config_border_width(void)
{
        return g_border_width;
}

int config_master_size(void)
{
        return g_master_size;
}

float config_master_ratio(void)
{
        return g_master_ratio;
}

int config_snap(void)
{
        return g_snap;
}
