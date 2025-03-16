// Define the directory containing the .tif images
inputDir = "Z:\\Gladfelter_rotation\\Michael_Ursa\\20240620_NaCl-gradient_24hr\\0_data\\";

// Get list of all .tif files in the directory
list = getFileList(inputDir);

// Loop through each file
for (i = 0; i < list.length; i++) {
    if (endsWith(list[i], ".tif")) {
        // Open the image
        open(inputDir + list[i]);

        // Get the title of the image
        imageTitle = getTitle();
        basename = File.getNameWithoutExtension(imageTitle);
        outputDir = inputDir + basename + "\\";
        if (!File.exists(outputDir)) {
        	File.makeDirectory(outputDir);
        }

        // Get the number of time points
        stackSize = nSlices;
        run("Stack to Images");

        // Loop through each time point
        for (t = 1; t <= stackSize; t++) {
            // Select the image for the current time point
            tFormatted = d2s(t, 0);
            while (lengthOf(tFormatted) < 4) {
                tFormatted = "0" + tFormatted;
            }
            basename_t = basename + "-" + tFormatted;
            selectWindow(basename_t);

            // Run the image processing steps
            run("Duplicate...", "title="+basename_t+"-1");
            run("Gaussian Blur...", "sigma=50");

            // Assuming the current image is used for subtraction as well
            // Ensure to adjust the titles in the following line accordingly
            imageCalculator("Subtract create 32-bit", basename_t, basename_t + "-1");

            // Select the result image
            resultTitle = basename_t + "_subtr_bkg";
            selectImage("Result of " + basename_t);
            rename(resultTitle);
            

            // Convert to 16-bit and apply other processing steps
            setOption("ScaleConversions", true);
            run("16-bit");
            run("Enhance Contrast", "saturated=0.35");
            run("Apply LUT");

            // Save the processed image
            saveAs("Tiff", outputDir + resultTitle + ".tif");

            // Close the original stack images
        	close(basename);
        	close(basename_t);
        	close(resultTitle);
        }

        // Close the original stack images
        close("*");
    }
}


