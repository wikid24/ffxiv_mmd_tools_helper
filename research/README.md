Physically-based objects are never 'animated' like you would for a regular bone. When physics are turned on, gravity does the work to move them. This is where rigid bodies and joints come in. When you import a rig from FFXIV, it should already have bones and meshes, but there are no rigid bodies or joints attached. You need to add them.

The relationship between rigid bodies, bones, meshes, and joints is important. Bones control a mesh and how it deforms. However, if you turn physics on, rigid bodies control a bone (and therefore, the mesh). The important thing about that rigid bodies is that they have "gravity" properties, therefore depending on the settings applied, they will move according to the gravity parameters set on them, and will affect other rigid bodies when they collide. Joints will pin rigid bodies together so that they move as if the rigid bodies are attached, and they control how much rigid bodies are allowed to move/rotate in relation to eachother.

   - Let's say your FFXIV model has a tail. 
   - If you want physics to work you need to create a 'physics-based' rigid body (more on that later), ONE FOR EACH BONE on the tail. Once you do this, your tail will now adhere to the rigid body's physics and it will (mostly) ignore the parent/child relationship from bones. If you press the 'play' button in blender and physics are turned on at this point, the tail rigid bodies will fall due to gravity and the bones/mesh will go along with it.
   - It is important to note that there is no parent/child relationship between rigid bodies like there are for bones. To make sure that rigid bodies will stay togehter, you need to create 'joints' between the rigid bodies.
   - Joints are for connecting each 'physics-based' rigid body to EACH OTHER. You connect each rigid body to eachother via joints, and finally the tail stem is attached via a joint to a "non-moving" 'collision-based' rigid body, so that it will stick to the body.
   - You have to tune the parameters on the rigid bodies and joints individually to make sure that when physics are applied, that it will bend and move according to how it would in real life.

Once you add rigid bodies and joints to your model, the physics will work properly. 
   

# Rigid Bodies
- Rigid Bodies are added to bones, and cover the entirety of your model's mesh.   
- The entire purpose of rigid bodies is so that you can apply physics SOME parts of your model, so that some parts will have physics applied (such as hair and skirts) and other parts will serve as collision objects so that they are not passed through.
- Rigid bodies 'mostly' cover the entireity of your model's mesh to ensure that all physics rules are applied. 
- There are two types of rigid bodies: "collision-based" rigid bodies and "physics-based" rigid bodies
   - "Collison-based" rigid bodies are used for making sure that physics-based based rigid bodies don't pass through them
      - Pretty much the human skeleton will be all collision-based rigid bodies, where as hair, skirts, breasts, tails will be physics-based.
      - For the human skeletion, there is usually a 1:1 bone to rigid body mapping. However, there are some places on the human body where one rigid body isn't enough.
      - For example, the upper body bone usually has 2 or more rigid bodies attached to it. This is because the shape of one rigid body Isn't enough to cover the entire mesh
   - "Physics-based" rigid bodies contain properties that are important for gravity:
      - When it comes to gravity, you want some rigid bodies on a rigid body 'chain' to be heavier than others:
          - You'd want the bottom of the skirt to be heavier than the top of the skirt (to make sure it retains it's form and doesn't go floating out to space)
          - You'd want the top of hair to be heavier than the bottom of the hair (to make sure that hair 'whips' around realistically)
- Rigid Bodies can be sorted into groups (namely, groups 0 to 15). When assigned to a group, you can create apply group 'masks' to a rigid body, so that when a rigid body collides, it can ignore the collision and pass right through it. This is especially useful when you want SOME rigid bodies to collide, but some you do not. For example, let's say you have a character with two long ponytails on each side of the head. The skeleton is assigned to Group 0, the left ponytail chain is assigned to  to Group 5 and the right ponytail chain is assigned to Group 6. Both ponytails need to collide with the skeleton, however it looks weird if they collide with eachother. Therefore on the rigid bodies in group 5, you tell them to ignore Group 6 (via using the masking option) and likewise for Group 6, you tell them to ignore group 5. This will make the pigtails to pass through eachother, however they will still both collide with the skeleton.

![image](https://user-images.githubusercontent.com/19479648/215564617-88770c4d-b195-45d5-8a18-4e0f0e3b947f.png)

![image](https://user-images.githubusercontent.com/19479648/215577795-103c4fb6-77b7-4003-8cca-4d5450e365c6.png)



# Joints
-  Joints need to be added to rigid bodies with physics such as hair, skirts and tails. They attach the rigid bodies to eachother so that they don't just 'fall off' and hit the floor.
-  Joints are used to attach "physics-based" rigid bodies together, as well as to pin it to a "collision-based" rigid body so it doesn't fall off your model (such as hair, tails, skirts, breasts and earrings).
-  Joints control physics "sway" such as how far the rigid body is allowed to bend.
    - Tails (if you'd want to be very stiff) so you'd limit them to +/- 5 degrees or so in all directions (so x,y,z) would apply the same amount.
    - Skirts (if you'd want to be very loose) so you'd allow them to bend +/- 100 degrees possibly. X,Y amd Z depends on which direction you'd want them to go in (they should all be different).
    - Hair is somewhere in-between the two.
    - Accessories such as earrings is also a toss up
    - Breasts (if you want breast jiggle) +/- 5 to 10 degrees in all directions seems about right? IDK never got that far yet.
-  Each joint 'chain' should always be connected to one rigid body that is NOT physics based.
    - For example, on a tail, you'd want one 'tail stem' (collision-based) rigid body that doesn't move. The first joint would be attached to the 'tail stem' and the movable tail rigid body
    - Joints that don't have a chain (such as earrings or breasts) need to be attached to a rigid body that doesn't move too.
- Joints have the switch to enable whether collisions with other rigid bodies are respected or not ("Disable collisions" checkbox)
    - Tails seem to have 'Disable Collisions' checked
    - Hair (depending on if it will cause issues and where it is located), you'd need to decide if collilison is needed or not.
    - Same goes with free-floating accessories such as earrings.

![image](https://user-images.githubusercontent.com/19479648/215570041-21a0cb3f-c720-4fe4-a2e1-0e809e1968ef.png)


![image](https://user-images.githubusercontent.com/19479648/215570786-67424d37-b7dc-4337-a4b4-1203b349db79.png)


## Skirts
It appears there are two kinds of joints on skirts: vertical joints and horizontal joints

### Vertical Joints :
-  The first Vertical Joint attaches from lower body to top of skirts, and continues all the way down to the bottom of the rigid body chain (following the bone's chain)
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



