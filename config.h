/* -*- mode: c; -*- */

#ifndef WM_CONFIG_H
#define WM_CONFIG_H

#include <defs.h>

#include <X11/Xlib.h>
#include <X11/cursorfont.h>

const char *config_fontname(void);

const char **config_colors(void);
size_t config_colors_size(void);

const int *config_cursors(void);
size_t config_cursors_size(void);

const char **config_termcmd(void);
const char **config_screenshotcmd(void);

size_t config_margin(void);

int config_showbar(void);
int config_border_width(void);

int config_master_size(void);
float config_master_ratio(void);

int config_snap(void);

#endif /* WM_CONFIG_H */
