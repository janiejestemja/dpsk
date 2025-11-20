import sys

model_flag = None
model_flags = ["tiny", "hrms", "dpsk"]

if len(sys.argv) == 2 and sys.argv[1] in model_flags:
    model_flag = sys.argv[1]
else:
    raise NotImplementedError("Please specify a valid model flag: " + ", ".join(model_flags))

match model_flag:
    case "tiny":
        from .tiny.tiny import Prompt
    case "hrms":
        from .hrms.hrms import Prompt
    case "dpsk":
        from .dpsk.dpsk import Prompt
    case _:
        raise NotImplementedError("Please specify a valid model flag: " + ", ".join(model_flags))

__all__ = ["Prompt"]