# fileName : plugins/dm/callBack/file_process/drawPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/drawPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz

async def drawPDF(input_file: str, cDIR: str) -> ( bool, str ):
    """
    This helps you to fetch 3D graphics from a PDF file. If the PDF document contains 3D models or graphics,
    and can extract and return those 3D elements for further processing or viewing. This can be useful for tasks
    such as visualizing or analyzing 3D models, or integrating them into other applications or workflows.
    
    parameter:
        input_file : Here is the path of the file that the user entered
        cDIR       : This is the location of the directory that belongs to the specific user.
    
    return:
        bool        : Return True when the request is successful
        output_path : This is the path where the output file can be found.
    """
    try:
        output_path = f"{cDIR}/outPut.pdf"
        with fitz.open(input_file) as iNPUT:
            with fitz.open() as oUTPUT:                     # empty output PDF
                for page in iNPUT:
                    paths = page.get_drawings()
                    outpage = oUTPUT.new_page(width=page.rect.width, height=page.rect.height)
                    shape = outpage.new_shape()
                    for path in paths:
                        for item in path["items"]:          # these are the draw commands
                            if item[0] == "l":              # line
                                shape.draw_line(item[1], item[2])
                            elif item[0] == "re":           # rectangle
                                shape.draw_rect(item[1])
                            elif item[0] == "qu":           # quad
                                shape.draw_quad(item[1])
                            elif item[0] == "c":            # curve
                                shape.draw_bezier(item[1], item[2], item[3], item[4])
                            else:
                                raise ValueError("unhandled drawing", item)
                        shape.finish(
                            fill = path["fill"],                            # fill color
                            color = path["color"],                          # line color
                            dashes = path["dashes"],                        # line dashing
                            even_odd = path.get("even_odd", True),          # control color of overlaps
                            closePath = path["closePath"],                  # whether to connect last and first point
                            lineJoin = path["lineJoin"],                    # how line joins should look like
                            lineCap = max(path["lineCap"]),                 # how line ends should look like
                            width = path["width"],                          # line width
                            stroke_opacity = path.get("stroke_opacity", 1), # same value for both
                            fill_opacity = path.get("fill_opacity", 1),     # opacity parameters
                        )
                shape.commit()
                oUTPUT.save(output_path, garbage = 3, deflate = True)
        return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab
