# Rejected initial proxy attempts

The first full render stalled after CUDA error 700. The following chapter attempt exported CH01-CH03 but also hit CUDA error 700 in CH04. Inspection of the actual chapter files then found a separate composition error: effect-mask links used the image output name `Output` instead of the mask output name `Mask`. This made some accent backgrounds fill the frame and invalidated that partial preview.

The three initial chapter files and their partial preview were moved to `C:/Users/KK/Movies/HIA_VIDEO007_R1/REJECTED_MASK_ERROR/`. They are REJECT, not review candidates. `REJECTED_RENDER_RESULTS_PRE_MASK_FIX.json` is historical attempt evidence, not a PASS.

Corrected native files use `Source = "Mask"`, nonzero lower bounds for mask geometry, and `UseGPU = 0` for Fusion operators. These changes require a fresh native render and visual verification; no success is inferred from the source files alone. The approved WAV has not been modified.
