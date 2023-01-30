# Rigid Bodies
	- Rigid Bodies are added to bones, and cover the entirety of your model's mesh.
	- The entire purpose of rigid bodies is so that you can apply physics SOME parts of your model, so that some parts will have physics applied (such as hair and skirts) and other parts will serve as collision objects so that they are not passed through.
	- Rigid bodies 'mostly' cover the entireity of your model's mesh to pretty much ensure that all physics rules are applied. 
	- There are two types of rigid bodies: collision-based rigid bodies and physics-based rigid bodies
		- Collison-based rigid bodies are used for making sure that physics-based based rigid bodies don't pass through them
			- Pretty much the human skeleton will be all collision-based rigid bodies, where as hair, skirts, breasts, tails will be physics-based.
			- For the human skeletion, there is usually a 1:1 bone to rigid body mapping. However, there are some places on the human body where one rigid body isn't enough.
			- For example, the upper body bone usually has 2 or more rigid bodies attached to it. This is because the shape of one rigid body Isn't enough to cover the entire mesh
		- Physics-based rigid bodies contain properties that are important for gravity:
			- When it comes to gravity, you want some rigid bodies to be heavier than others:
				- You'd want the bottom of the skirt to be heavier than the top of the skirt (to make sure it retains it's form and doesn't go floating out to space)
				- You'd want the top of hair to be heavier than the bottom of the hair (to make sure that hair 'whips' around realistically)



# Joints
	-  Joints need to be added to rigid bodies with physics such as hair, skirts and tails.
	-  Joints are used to attach rigid bodies that will have physics applied to them (such as hair, tails, skirts, breasts and earrings).
	-  Joints control physics "sway" such as how far the rigid body is allowed to bend.
		- Tails (if you'd want to be very stiff) so you'd limit them to +/- 5 degrees or so in all directions (so x,y,z) would apply the same amount.
		- Skirts (if you'd want to be very loose) so you'd allow them to bend +/- 100 degrees possibly. X,Y amd Z depends on which direction you'd want them to go in (they should all be different).
		- Hair is somewhere in-between the two.
		- Accessories such as earrings is also a toss up
		- Breasts (if you want breast jiggle) +/- 5 to 10 degrees in all directions seems about right? IDK never got that far yet.
	-  Each joint 'chain' should always be connected to one rigid body that is NOT physics based.
		- For example, on a tail, you'd want one 'tail stem' rigid body that doesn't move. The first joint would be attached to the 'tail stem' and the movable tail rigid body
		- Joints that don't have a chain (such as earrings or breasts) need to be attached to a rigid body that doesn't move too.)
	- Joints have the switch to enable whether collisions with other rigid bodies are respected or not ("Disable collisions" checkbox)
		- Tails seem to have 'Disable Collisions' checked
		- Hair (depending on if it will cause issues and where it is located), you'd need to decide if collilison is needed or not.
		- Same goes with free-floating accessories such as earrings


##Skirts
	It appears there are two kinds of joints on skirts: vertical joints and horizontal joints

### Vertical Joints :
	-  First Vertical Joint attaches from lower body to top of skirts
	-  Disable collisions is unchecked
	-  Uses Angular limits and spring angular
		#### Lisa Genshin Model
		- angular limit: -30, -30, -10, 7, 30, 10 (lower x, lower y, lower z, upper x, upper y, upper z)
		- spring linear: 10,10,10
		- spring angular: 110, 110, 110

### Horizontal Joints
	- Attaches rigid bodies to eachother horizontally. Used to prevent horizontal 'stretching' since we want skirts to somewhat keep their form.
	- Disable collisions is checked
	- Uses Linear limits, spring linear and spring angular
		#### Lisa Genshin Model
		- linear limit: -0.0201,-0.0201,-0.0201,0.0201,0.0201,0.0201 (lower x, lower y, lower z, upper x, upper y, upper z)
		- spring linear: 10,10,10
		- spring angular: 100, 100, 100



