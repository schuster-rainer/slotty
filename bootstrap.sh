virtualenv .slotty
source .slotty/bin/activate

#ARCHFLAGS: macosx specific
#Xcode 5.1 changed the way clang treats invalid compiler options.
#many python or ruby native extensions don't treat this change yet ... 
#in the meantime we switch off the error
ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install --upgrade -r requirements.txt
pip install --upgrade -r requirements-dev.txt
pip install --upgrade -e .

