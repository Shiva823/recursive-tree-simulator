# 🌳 Recursive Tree Growth Simulator

An interactive computer graphics visualization that demonstrates natural tree growth patterns using recursive algorithms and L-systems principles. Watch trees grow from seedlings to full maturity with realistic seasonal transformations and dynamic environmental effects.

<img src="screenshot.png" alt="Tree Simulator Demo" width="600">

## 🎯 Project Overview

This project was developed as a mini-project for a Computer Graphics course to explore and demonstrate fundamental concepts in computational geometry, recursive algorithms, and interactive visualization. The simulator generates fractal tree structures using mathematical recursion and provides an intuitive interface for real-time parameter manipulation.

## ✨ Key Features

### 🌿 Recursive Tree Generation
- **L-System Inspired Algorithm**: Uses formal grammar rules for organic branching patterns
- **Fractal Geometry**: Self-similar structures at different scales
- **Configurable Parameters**: Adjust branching angles, recursion depth, and branch proportions
- **Dynamic Growth**: Real-time tree generation with customizable complexity

### 🌸 Four Seasonal Modes

#### Spring
- Light green blooming leaves
- Fresh, vibrant color palette
- Represents new growth and renewal

#### Summer
- Deep green full foliage
- Dense leaf coverage
- Peak growth representation

#### Autumn
- Orange, red, and brown leaves
- **Animated falling leaves** with physics simulation
- Wind drift effects for realistic movement
- Continuous leaf spawning and removal

#### Winter
- Bare branch structure
- Showcases the underlying recursive tree skeleton
- Clean, minimalist aesthetic

### 📈 Animated Growth Visualization
- **Progressive rendering**: Watch branches emerge from trunk to tips
- **Smooth animation**: Frame-by-frame growth simulation
- **Restart capability**: Reset and replay growth sequence
- **Adjustable speed**: Control growth rate for detailed observation

### 🎛️ Interactive Parameter Controls

Real-time sliders for customization:
- **Branch Angle** (10° - 60°): Controls spread and tree shape
  - Narrow angles → Columnar trees (poplar-like)
  - Wide angles → Spreading trees (oak-like)
- **Recursion Depth** (5 - 13): Determines tree complexity
  - Lower values → Simple, young trees
  - Higher values → Complex, mature trees
- **Branch Length Ratio** (50% - 80%): Child branch proportion
  - Lower values → Compact trees
  - Higher values → Elongated branches
- **Trunk Length** (80 - 200): Initial trunk height

### 🍂 Physics-Based Particle System
- Falling leaves in autumn with:
  - Gravity simulation
  - Wind drift effects
  - Rotation animation
  - Screen boundary detection and recycling

## 🎮 Controls

| Input | Action |
|-------|--------|
| `1` | Switch to **Spring** season |
| `2` | Switch to **Summer** season |
| `3` | Switch to **Autumn** season (enables falling leaves) |
| `4` | Switch to **Winter** season (bare branches) |
| `SPACE` | **Restart growth animation** from beginning |
| **Right-side sliders** | Adjust tree parameters in real-time |

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone the repository:**
```bash
   git clone https://github.com/Shiva823/recursive-tree-simulator.git
   cd recursive-tree-simulator
```

2. **Install dependencies:**
```bash
   pip install -r requirements.txt
```

3. **Run the simulator:**
```bash
   python tree_simulator.py
```

The application window will open immediately, and you'll see the tree begin growing automatically.

## 📦 Dependencies
```
pygame==2.5.2          # Graphics rendering and game loop
pygame-gui==0.6.9      # UI elements (sliders and labels)
```

All dependencies are listed in `requirements.txt` for easy installation.

## 🎓 Educational Objectives

This project demonstrates core Computer Graphics concepts:

### Algorithms & Data Structures
- **Recursive algorithms**: Tree traversal and rendering
- **Stack-based execution**: Understanding recursion depth
- **Coordinate transformations**: 2D rotation and translation

### Graphics Programming
- **2D rendering pipeline**: Line drawing and shape filling
- **Transformation matrices**: Rotation, translation, scaling
- **Frame-based animation**: Smooth visual transitions
- **Color theory**: Seasonal palettes and gradients

### Mathematical Concepts
- **Trigonometry**: Branch angle calculations using sine/cosine
- **Fractal geometry**: Self-similar patterns at multiple scales
- **Parametric equations**: Branch endpoint calculations
- **Exponential decay**: Branch thickness reduction

### Interactive Systems
- **Event-driven programming**: Keyboard and slider inputs
- **Real-time parameter adjustment**: Immediate visual feedback
- **GUI integration**: User interface design

### Physics Simulation
- **Particle systems**: Falling leaf management
- **Simple physics**: Gravity and wind forces
- **Collision detection**: Screen boundary checking

## 🛠️ Technical Implementation

### Tree Generation Algorithm
```
Function DrawBranch(x, y, length, angle, depth):
    If depth = 0:
        Return
    
    Calculate endpoint using:
        end_x = x + length × cos(angle)
        end_y = y + length × sin(angle)
    
    Draw line from (x, y) to (end_x, end_y)
    
    If depth ≤ 3:
        Draw leaf at endpoint
    
    Recursively call:
        DrawBranch(end_x, end_y, length × ratio, angle - branch_angle, depth - 1)
        DrawBranch(end_x, end_y, length × ratio, angle + branch_angle, depth - 1)
```

### Growth Animation

The growth animation works by incrementally increasing the maximum recursion depth rendered:
- Frame 1: Draw only trunk (depth = 1)
- Frame 2: Draw trunk + first branches (depth = 2)
- Frame N: Draw up to depth N
- Continues until full recursion depth reached

### Seasonal System

Each season defines:
- Background color (sky gradient)
- Leaf color palette (multiple shades for variety)
- Leaf visibility flag
- Special effects (falling leaves for autumn)

## 📸 Screenshots

### Spring Season - Fresh Growth
<img src="SPRING.png" alt="Spring Season" width="600">
*Light green leaves representing new growth and renewal*

### Summer Season - Full Foliage
<img src="SUMMER.png" alt="Summer Season" width="600">
*Dense, dark green leaves at peak growth*

### Autumn Season - Falling Leaves
<img src="autumn.png" alt="Autumn Season" width="600">
*Orange and red leaves with animated falling effect and wind simulation*

### Winter Season - Bare Branches
<img src="WINTER.png" alt="Winter Season" width="600">
*Bare tree structure showcasing the recursive branching pattern*

## 🔬 Experimentation Ideas

Try these parameter combinations for interesting results:

### Realistic Trees
- **Oak**: Angle 45°, Depth 10, Length 65%, Trunk 120
- **Pine**: Angle 20°, Depth 12, Length 70%, Trunk 150
- **Willow**: Angle 35°, Depth 11, Length 75%, Trunk 100

### Abstract Patterns
- **Symmetric**: Angle 30°, Depth 13, Length 67%, Trunk 120
- **Wide Spread**: Angle 60°, Depth 8, Length 55%, Trunk 90
- **Tall & Narrow**: Angle 15°, Depth 10, Length 70%, Trunk 180

## 📝 Code Structure
```
tree_simulator.py
│
├── Imports & Initialization
├── Color Definitions (seasonal palettes)
├── FallingLeaf Class
│   ├── __init__: Initialize leaf properties
│   ├── update: Apply physics (gravity, wind)
│   └── draw: Render leaf particle
│
├── draw_branch_animated: Recursive tree drawing
├── spawn_initial_leaves: Autumn leaf generation
├── UI Elements: Sliders and labels
│
└── Main Game Loop
    ├── Event Handling (keyboard, sliders)
    ├── Growth Animation Update
    ├── Season Selection
    ├── Tree Rendering
    ├── Particle System Update (autumn)
    └── Display Update
```

## 🎨 Customization Guide

### Adding New Seasons

1. Define color palette in global constants
2. Add new case in season selection
3. Optionally add unique visual effects

### Modifying Tree Shape

Adjust these constants:
- `branch_angle`: Affects spread
- `branch_length_ratio`: Controls proportions
- `recursion_depth`: Changes complexity

### Adding Effects

The modular structure allows easy addition of:
- Different leaf shapes
- Background animations
- Additional particle effects
- Sound effects

## 🐛 Known Limitations

- Maximum recursion depth limited to 13 for performance
- Falling leaves use simple physics (no turbulence)
- 2D visualization only (no 3D perspective)
- Fixed window size (1000×700 pixels)

## 🚧 Future Enhancement Ideas

- [ ] 3D tree generation with OpenGL
- [ ] Export tree as SVG/PNG file
- [ ] Wind speed slider for autumn
- [ ] Day/night cycle with lighting
- [ ] Multiple tree presets (oak, pine, palm, etc.)
- [ ] Procedural texture mapping on branches
- [ ] Sound effects for seasons
- [ ] Save/load custom tree configurations
- [ ] Bird/butterfly particles in spring/summer

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution
- Performance optimization
- Additional visual effects
- Code refactoring
- Documentation improvements
- Bug fixes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ⚠️ Liability and warranty limitations

## 👨‍💻 Author

    Shiva823
- GitHub: [Shiva823](https://github.com/Shiva823)
- Project Link: [https://github.com/Shiva823/recursive-tree-simulator](https://github.com/Shiva823/recursive-tree-simulator)

## 🙏 Acknowledgments

- **L-Systems Theory**: Aristid Lindenmayer's work on formal grammars for plant modeling
- **Pygame Community**: For excellent documentation and examples
- **Computer Graphics Course**: For providing the learning opportunity
- **Fractal Geometry**: Benoit Mandelbrot's work on self-similar structures

## 📚 References & Further Reading

- [L-Systems on Wikipedia](https://en.wikipedia.org/wiki/L-system)
- [The Algorithmic Beauty of Plants](http://algorithmicbotany.org/papers/#abop) - Prusinkiewicz & Lindenmayer
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Fractal Trees - Nature of Code](https://natureofcode.com/book/chapter-8-fractals/)

## 💡 Learning Outcomes

By exploring this project, I understood:
- How recursion creates complex patterns from simple rules
- The relationship between mathematics and natural forms
- Real-time graphics rendering techniques
- Interactive application development
- Physics simulation basics
- UI/UX design for educational software

---


**Made with 🌳 and ❤️ for Computer Graphics education**

*Last Updated: January 2026*