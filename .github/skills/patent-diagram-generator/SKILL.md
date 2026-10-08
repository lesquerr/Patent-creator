---
name: patent-diagram-generator
description: "Create patent-style technical diagrams including flowcharts, block diagrams, and system architectures using Graphviz with reference numbering"
---

## Using the connected MCP server

In Copilot, connect to the configured `patent-creator` server with `/mcp` and restart Copilot after configuration changes. Discover the exposed tools and parameter schemas from that server. Invoke tools as attached MCP calls with named arguments matching the discovered schema. Server-qualified aliases vary by runtime, so invoke tools through Copilot's discovered MCP interface rather than hard-coding an alias or treating internal Python classes as exposed tools.
# Patent Diagram Generator Skill

Create patent-style technical diagrams including flowcharts, block diagrams, and system architectures using Graphviz.

## When to Use

Invoke this skill when users ask to:
- Create flowcharts for method claims
- Generate block diagrams for system claims
- Draw system architecture diagrams
- Create technical illustrations for patents
- Add reference numbers to diagrams
- Generate patent figures

## What This Skill Does

1. **Flowchart Generation**:
   - Method step flowcharts
   - Decision trees
   - Process flows with branches
   - Patent-style step numbering

2. **Block Diagram Creation**:
   - System component diagrams
   - Hardware architecture diagrams
   - Software module diagrams
   - Component interconnections

3. **Custom Diagram Rendering**:
   - Render Graphviz DOT code
   - Support multiple formats (SVG, PNG, PDF)
   - Multiple layout engines (dot, neato, fdp, circo, twopi)

4. **Patent-Style Formatting**:
   - Add reference numbers (10, 20, 30, etc.)
   - Use clear labels and connections
   - Professional formatting for USPTO filing

## Required Dependencies

This skill requires Graphviz to be installed:

**Windows**:
```powershell
choco install graphviz
```

**Python Package**:
```powershell
& .\.venv\Scripts\python.exe -m pip install graphviz
```

## How to Use

When this skill is invoked:

1. Call the attached MCP tool `check_diagram_tools_status`. Install the
   Graphviz executable if needed, then verify it with `dot -V`.

2. Call the attached MCP tool `create_flowchart` with named arguments
   `steps`, `filename`, `output_format`, and optional `output_dir`. Decision
   branches can use labeled next-step objects:
   ```text
   create_flowchart(
       steps=[
           {"id": "start", "label": "Start", "shape": "ellipse", "next": ["step1"]},
           {"id": "step1", "label": "Initialize System", "shape": "box", "next": ["decision"]},
           {"id": "decision", "label": "Is Valid?", "shape": "diamond", "next": [
               {"id": "step2", "label": "Yes"}, {"id": "error", "label": "No"}
           ]},
           {"id": "step2", "label": "Process Data", "shape": "box", "next": ["end"]},
           {"id": "error", "label": "Handle Error", "shape": "box", "next": ["end"]},
           {"id": "end", "label": "End", "shape": "ellipse", "next": []},
       ],
       filename="method_flowchart",
       output_format="svg",
   )
   ```

3. Call `create_block_diagram` with named arguments `blocks`, `connections`,
   `filename`, `output_format`, and optional `output_dir`:
   ```text
   create_block_diagram(
       blocks=[
           {"id": "input", "label": "Input\\nSensor", "type": "input"},
           {"id": "cpu", "label": "Central\\nProcessor", "type": "process"},
           {"id": "memory", "label": "Memory\\nStorage", "type": "storage"},
           {"id": "output", "label": "Output\\nDisplay", "type": "output"},
       ],
       connections=[
           ["input", "cpu", "raw data"], ["cpu", "memory", "store"],
           ["memory", "cpu", "retrieve"], ["cpu", "output", "processed data"],
       ],
       filename="system_diagram",
       output_format="svg",
   )
   ```

4. Call `render_diagram` with named arguments `dot_code`, `filename`,
   `output_format`, optional `engine`, and optional `output_dir`:
   ```text
   render_diagram(
       dot_code="digraph PatentSystem { rankdir=LR; Input -> Processor [label=\"data\"]; Processor -> Output [label=\"result\"]; }",
       filename="custom_diagram",
       output_format="svg",
       engine="dot",
   )
   ```

5. Call `add_diagram_references` with named arguments `svg_path` and
   `reference_map`:
   ```text
   add_diagram_references(
       svg_path="diagrams/system_diagram.svg",
       reference_map={
           "Input Sensor": 10,
           "Central Processor": 20,
           "Memory Storage": 30,
           "Output Display": 40,
       },
   )
   ```

## Diagram Templates

Call the native `get_diagram_templates` tool. Available templates:
# - simple_flowchart: Basic process flow
# - system_block: System architecture
# - method_steps: Sequential method
# - component_hierarchy: Hierarchical structure
```

## Shape Types

### Flowchart Shapes
- `ellipse`: Start/End points
- `box`: Process steps
- `diamond`: Decision points
- `parallelogram`: Input/Output operations
- `cylinder`: Database/Storage

### Block Diagram Types
- `input`: Input devices/sensors
- `output`: Output devices/displays
- `process`: Processing units
- `storage`: Memory/storage
- `decision`: Control logic
- `default`: General components

## Layout Engines

- `dot`: Hierarchical (top-down/left-right)
- `neato`: Spring model layout
- `fdp`: Force-directed layout
- `circo`: Circular layout
- `twopi`: Radial layout

## Output Formats

- `svg`: Scalable Vector Graphics (best for editing)
- `png`: Raster image (good for viewing)
- `pdf`: Portable Document Format (USPTO compatible)

## Patent-Style Reference Numbers

Convention:
- Main components: 10, 20, 30, 40, ...
- Sub-components: 12, 14, 16 (under 10)
- Elements: 22, 24, 26 (under 20)

Example labeling:
```
"Input Sensor (10)"
"  - Detector Element (12)"
"  - Signal Processor (14)"
"Central Unit (20)"
"  - CPU Core (22)"
"  - Cache (24)"
```

## Presentation Format

When creating diagrams:

1. **Describe what will be generated**:
   "Creating a flowchart for the authentication method with 5 steps..."

2. **Generate the diagram**:
   Invoke the appropriate attached MCP diagram tool with named arguments
   matching its discovered schema.

3. **Show file location**:
   Report the returned `path` exactly. Tool output paths resolve under the
   repository working directory.

4. **List reference numbers** (if added):
   ```
   Reference Numbers:
   - Input Module (10)
   - Processing Unit (20)
   - Output Interface (30)
   ```

## Common Use Cases

1. **Method Claims** → Flowcharts
   - Show sequential steps
   - Include decision branches
   - Number steps (S1, S2, S3...)

2. **System Claims** → Block Diagrams
   - Show components and connections
   - Use reference numbers
   - Indicate data flow directions

3. **Architecture Diagrams** → Custom DOT
   - Complex system layouts
   - Multiple interconnections
   - Hierarchical structures

## Error Handling

If Graphviz is not installed:
1. Check installation: `dot -V`
2. On Windows, install the Graphviz executable only when requested.
3. Check the Python package with
   `& .\.venv\Scripts\python.exe -m pip show graphviz`.
4. Re-run `check_diagram_tools_status` through the attached MCP server and
   retry the tool.

## MCP tools

`check_diagram_tools_status`, `get_diagram_templates`, `create_flowchart`,
`create_block_diagram`, `render_diagram`, and `add_diagram_references`.
Discover exact parameter schemas through Copilot's MCP interface; missing
Graphviz is returned as an explicit error.
