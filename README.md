# ranger-video-editor
&nbsp;&nbsp;&nbsp;&nbsp;Basic Ranger functions for cutting and splicing video clips.

## Usage
&nbsp;&nbsp;&nbsp;&nbsp;The basic workflow is `clip_start {[MM:]ss.ms}` ->  `clip_end {[MM:]ss.ms}` -> `clip_join {output_fname.VIDFMT}` where `VIDFMT` is a valid extension with a video mimetype.

&nbsp;&nbsp;&nbsp;&nbsp;Alternately use `clip_cut {[MM:]ss.ms} {[MM:]ss.ms}` where `arg[0]` is the start time `arg[1]` is the end time.

## Installation
```
git clone https://gitlab.com/Ragnyll/ranger-video-editor.git
cd ranger-video-editor
make install
```

## Uninstall
```
make uninstall
```
