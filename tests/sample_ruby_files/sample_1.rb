# This Ruby sample script can be found at:
# http://sandbox.mc.edu/~bennet/ruby/code/tk1_rb.html
# This script has 10 SLOC and 8 comments

# Import the library.
require 'tk'

# Root window.
root = TkRoot.new { title 'Push Me' }

# Add a label to the root window.
lab = TkLabel.new(root) { text "Push the Button" }

# Make it appear.
lab.pack

# Here's a button.  Also added to root by default.
TkButton.new {
  text "PUSH"
  command { print "Arrrrrrg!\n" }
  pack
}

Tk.mainloop
