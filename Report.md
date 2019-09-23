# ML Skill Test

**NOTE! Please rename the file *pre_install.bat.null* to *pre_install.bat* before you start.**

## How to use

Some packages need to be installed before using these functions or scripts. These packages can be installed as follows:

- If you use Windows, run pre_install.bat directly.

- If you use Linux, run *bash pre_install.sh* in the terminal.

The *create_digit_sequence* function is implemented in the *ocr_util.py*. It can be easily used as follow:

    # import the function from the model ocr_util
    from ocr_util import create_digit_sequence

    # define the params you would use
    number = '123456'
    width = 100
    min_spacing = 2
    max_spacing = 10

    # the seq_img is a NumPy array representing the image with the params.
    seq_img = create_digit_sequence(number, width, min_spacing, max_spacing)

- NOTE the parameters must be legal. If the width of the image is smaller than the minimum width needed, the *assert* in the source code will call an error. Obviously, you should ensure that the image width is bigger than or equal to *(n-1)\*min_spacing+n*, while *n* is the digits length of the number, otherwise there will be no space to display the number (even if the number is only 1 pixel). The min_spacing should be smaller than or equal to the max_spacing.

The command line utility (Python script) is implemented in the *gen_ocr_imgs.py*. By running the command: 

    python gen_ocr_imgs.py -h

you could see the help information: 

    usage: gen_ocr_imgs.py [-h] --path PATH --num NUM --digits DIGITS --width
                       WIDTH [--min_spacing MIN_SPACING]
                       [--max_spacing MAX_SPACING] [--form FORM]

    optional arguments:
    -h, --help            show this help message and exit
    --path PATH           The path you would save the image(s). (required)
    --num NUM             The amount of images you would create. (default: 1)
    --digits DIGITS       The number of the digits of every number you would
                            create. (required)
    --width WIDTH         The image width (in pixel). (required)
    --min_spacing MIN_SPACING
                            The minimum spacing between digits (in pixel).
                            (default: 0)
    --max_spacing MAX_SPACING
                            The maximum spacing between digits (in pixel).
                            (default: 28)
    --form FORM           The image format. (default: jpg)

The parameters are: 

--path: 

- Required. Considering that you may use this script to create a large number of images, if this parameter is not set to required and the default path would be set (such as the same level directory of script files), then it might generate a large number of image files in the path you do not want, which will have a negative impact on the cleanliness of the project directory, so this parameter is required.
- It specifies which directory you want to create images in.
- If the directory specified by the path does not exist, the script will create a new directory by the path.

--num: 

- It specifies how many pictures you want to create. The default value is 1.

--digits: 

- Required. At the beginning, I did not intend to design this parameter as required. When you don't specify it, the script will create random-digit images, but this will cause many problems. First, to determine the range of random-digit, you need to input two additional parameters representing the range (or use default values). At the same time, you need to determine the width of the picture. Then you will have to consider whether the relationship between these random lengths, width, min_spacing and max_spacing is legal or not. If not carefully considered, the illegal values in the process of creation will lead to errors. To avoid these unnecessary troubles, I set this parameter to required. This means that you can only create a batch of number images of the same digit length at a time, while the advantage is that if you set legal parameters at the beginning, you won't have to worry about making mistakes in the creation process. If you need to create a random-length image, you can call the script with random and legal parameters in an external program, and the legitimacy of those parameters can be easily controlled by the programmer himself.
- It specifies the number of digits in the image you create. 

--width

- Required
- The image width (in pixel).

--min_spacing

- The minimum spacing between digits (in pixel). (default: 0)

--max_spacing
- The maximum spacing between digits (in pixel). (default: 28)

--form
- The image format. (default: jpg)

## Detail of Implementation

The *create_digit_sequence* function is implemented in the *ocr_util.py*. A class named *DigitGenerator* is also contained. The function *DigitGenerator.gen_digit(digit: str)* is used to create an image representing the given digit which is randomly sampled from the MNIST dataset. The white areas on left and right sides in the original MNIST image are cropped. It returns an NumPy array representing the image.

In the *create_digit_sequence*, I firstly get all the digit images I need by using the *DigitGenerator*, then depending on the relation between image width, min_spacing, max_spacing, the length of the number and the total width of all the digit images, create the final image. Note that in the first *if* block, the digit images have to be compressed to make the final width and spacing size correct.

The command line utility (Python script) is implemented in the *gen_ocr_imgs.py*. Firstly, the argparse is used to parse all the command line parameters, then the *os.path.isdir()* and *os.mkdir* will be used to create a new folder if it doesn't exist. Finally, the random numbers are generated and the images will be obtained by  the function above. The opencv is used to write the images to the path you give.

In the folder named "ocr_imgs", there are five samples created by this tool.