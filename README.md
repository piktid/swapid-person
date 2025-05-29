<p align="center">
  <img src="https://studio.piktid.com/logo.svg" alt="SuperID by PiktID logo" width="150">
  </br>
  <h3 align="center"><a href="[https://studio.piktid.com](https://studio.piktid.com)">SwapID - Full Body Person Swap by PiktID</a></h3>
</p>


# SwapID - Full Body Person Swap 1.0.0
[![Official Website](https://img.shields.io/badge/Official%20Website-piktid.com-blue?style=flat&logo=world&logoColor=white)](https://piktid.com)
[![Discord Follow](https://dcbadge.vercel.app/api/server/FJU39e9Z4P?style=flat)](https://discord.com/invite/FJU39e9Z4P)

SwapID - Full Body Person Swap is an advanced GenAI tool designed to perform comprehensive person swapping in images using a revolutionary two-step process that ensures superior skin tone matching and seamless integration.

## About
SwapID utilizes a sophisticated two-step approach to achieve the most realistic person swaps possible:

### Two-Step Process:
1. **Full Body Generation**: The tool first identifies the person in your target image and generates a complete new body that matches the reference person's characteristics, including skin tone, build, and overall appearance.

2. **Face/Head Swap**: Using the newly generated body as the base, the tool then performs a precise face or head swap using the same reference image, ensuring perfect skin tone continuity and natural integration.

### Key Advantages:
- <ins>Superior Skin Tone Matching</ins>: The two-step process ensures perfect skin tone continuity between face and body
- <ins>Cross-Ethnicity Swapping</ins>: Successfully swap between people of different ethnicities (e.g., dark skin on light skin photos and vice versa)
- <ins>Natural Integration</ins>: The full body generation creates a cohesive base for the final face swap
- <ins>Advanced AI Processing</ins>: Leverages cutting-edge generative AI for realistic results

## Current Limitations
- **Single Person Images**: Currently optimized for images containing only one person
- **Target Person Detection**: The tool automatically detects and processes the primary person in the image

## Getting Started

The following instructions suppose you have already installed a recent version of Python. To use any PiktID API, an access token is required.

> **Step 0** - Register <a href="https://studio.piktid.com">here</a>. 10 credits are given for free to all new users.

> **Step 1** - Clone the SwapID - Full Body Person Swap repository
```bash
# Installation commands
$ git clone https://github.com/piktid/swapid-person.git
$ cd swapid-person
```

> **Step 2** - Export your email and password as environmental variables
```bash
$ export SWAPID_EMAIL={Your email here}
$ export SWAPID_PASSWORD={Your password here}
```

> **Step 3** - Run the main function with target and reference images
```bash
# Using URLs for both target and reference images
$ python3 main_full.py --target_url 'your-target-image-url' --reference_url 'your-reference-image-url' --body

# Using local file paths
$ python3 main_full.py --target_path '/path/to/target/image.jpg' --reference_path '/path/to/reference/image.jpg' --body

# Face-only swap (without full body generation)
$ python3 main_full.py --target_path '/path/to/target/image.jpg' --reference_path '/path/to/reference/image.jpg'
```

You can customize the generation with advanced parameters:

```bash
# Full body swap with custom parameters (e.g. including hair)
$ python3 main_full.py --target_path '/path/to/target.jpg' --reference_path '/path/to/reference.jpg' --body --hair --seed 12345 --swap_strength 0.55 --person_strength 0.9
```

## Available Parameters

### Input Parameters
- **target_path**: Local path to the target image file
- **target_url**: URL of the target image (used if no target_path provided)
- **reference_path**: Local path to the reference image file  
- **reference_url**: URL of the reference image (used if no reference_path provided)
- **target_name**: Target image code name (overrides target_path if provided)
- **reference_name**: Reference image code name (overrides reference_path if provided)

### Generation Parameters
- **seed**: Random seed for reproducible results
- **prompt**: Target image description for enhanced generation
- **controlnet_scale**: Resemblance with target face (range 0-2)
- **guidance_scale**: Generation guidance scale (range 1-20)

### Swap Control Parameters
- **--hair**: Include hair in the swap (head-swap mode)
- **swap_strength**: Face similarity level with reference (range 0-1)
- **id_face**: Index of the face to swap in target image (default: 0)

### Person Edit Parameters
- **--body**: Enable full body swap (recommended for best results)
- **person_strength**: Similarity with reference person (range 0-1)
- **var_strength**: Creativity level in generation (range 0-1)
- **id_person**: Index of person to modify in target image (default: 0)

## Usage Examples

### Basic Full Body Swap
```bash
python3 main_full.py --target_path './images/target.jpg' --reference_path './images/reference.jpg' --body
```

### Face-Only Swap
```bash
python3 main_full.py --target_path './images/target.jpg' --reference_path './images/reference.jpg'
```

### Advanced Full Body Swap with Hair
```bash
python3 main_full.py --target_path './images/target.jpg' --reference_path './images/reference.jpg' --body --hair --swap_strength 0.55 --person_strength 0.9 --controlnet_scale 0.1
```

## Contact
office@piktid.com
