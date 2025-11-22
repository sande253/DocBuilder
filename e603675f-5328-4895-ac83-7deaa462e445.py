from manim import *

class SimpleDFAExplanation(Scene):
    def construct(self):
        # --- 1. Introduction --- 
        title = Text("Deterministic Finite Automaton (DFA)", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        intro_text = Text(
            "A DFA recognizes patterns in strings using states and transitions.",
            font_size=28
        ).next_to(title, DOWN, buff=0.5)
        self.play(Write(intro_text))
        self.wait(1.5)
        self.play(FadeOut(intro_text))

        # --- 2. Define States --- 
        # State Q0 (initial state)
        q0_circle = Circle(radius=0.8, color=BLUE, fill_opacity=0.2)
        q0_text = Text("Q0", color=WHITE).move_to(q0_circle.get_center())
        state_q0 = VGroup(q0_circle, q0_text)

        # State Q1 (accepting state)
        q1_circle_outer = Circle(radius=0.8, color=GREEN, fill_opacity=0.2)
        q1_circle_inner = Circle(radius=0.7, color=GREEN, stroke_width=2) # Inner circle for accepting state
        q1_text = Text("Q1", color=WHITE).move_to(q1_circle_outer.get_center())
        state_q1 = VGroup(q1_circle_outer, q1_circle_inner, q1_text) # Outer circle is first for consistent indexing

        # Arrange states horizontally
        states = VGroup(state_q0, state_q1).arrange(RIGHT, buff=3).center()
        self.play(Create(states))
        self.wait(0.5)

        # Initial state indicator arrow
        start_arrow = Arrow(start=LEFT * 3, end=state_q0[0].get_left(), buff=0.1, color=YELLOW)
        start_label = Text("Start", font_size=24, color=YELLOW).next_to(start_arrow, LEFT)
        initial_indicator = VGroup(start_arrow, start_label)
        self.play(Create(initial_indicator))
        self.wait(0.5)

        # --- 3. Define Transitions --- 
        # Transition Q0 --a--> Q1
        arrow_q0_q1_a = Arrow(state_q0[0].get_right(), state_q1[0].get_left(), buff=0.1, color=ORANGE)
        label_q0_q1_a = Text("a", font_size=24, color=ORANGE).next_to(arrow_q0_q1_a, UP)
        transition_q0_q1_a = VGroup(arrow_q0_q1_a, label_q0_q1_a)

        # Transition Q0 --b--> Q0 (self-loop)
        # Create an Arc and add a tip to form the self-loop arrow
        loop_q0_b_path = Arc(start_angle=PI/2, angle=-PI, radius=0.7, arc_center=state_q0[0].get_center() + UP*0.7, color=ORANGE)
        arrow_q0_loop_b = loop_q0_b_path.add_tip(tip_length=0.2, at_start=False, tip_width=0.2)
        label_q0_loop_b = Text("b", font_size=24, color=ORANGE).move_to(arrow_q0_loop_b.get_top() + UP * 0.2)
        transition_q0_loop_b = VGroup(arrow_q0_loop_b, label_q0_loop_b)

        # Transition Q1 --a--> Q1 (self-loop)
        loop_q1_a_path = Arc(start_angle=PI/2, angle=-PI, radius=0.7, arc_center=state_q1[0].get_center() + UP*0.7, color=ORANGE)
        arrow_q1_loop_a = loop_q1_a_path.add_tip(tip_length=0.2, at_start=False, tip_width=0.2)
        label_q1_loop_a = Text("a", font_size=24, color=ORANGE).move_to(arrow_q1_loop_a.get_top() + UP * 0.2)
        transition_q1_loop_a = VGroup(arrow_q1_loop_a, label_q1_loop_a)

        # Transition Q1 --b--> Q0 (curved arrow below)
        arrow_q1_q0_b = CurvedArrow(state_q1[0].get_bottom(), state_q0[0].get_bottom(), angle=-PI/4, color=ORANGE)
        label_q1_q0_b = Text("b", font_size=24, color=ORANGE).next_to(arrow_q1_q0_b, DOWN)
        transition_q1_q0_b = VGroup(arrow_q1_q0_b, label_q1_q0_b)

        # Group all transitions
        transitions = VGroup(
            transition_q0_q1_a,
            transition_q0_loop_b,
            transition_q1_loop_a,
            transition_q1_q0_b
        )
        self.play(Create(transitions))
        self.wait(1)

        # --- 4. Group all DFA elements and reposition --- 
        dfa_diagram = VGroup(states, initial_indicator, transitions)
        self.play(dfa_diagram.animate.scale(0.8).to_edge(UP, buff=1.5).to_edge(LEFT, buff=1))
        self.wait(1)

        # --- 5. Process an input string --- 
        input_str = "babaa"
        input_label = Text("Input String:", font_size=32).next_to(dfa_diagram, RIGHT, buff=2).to_edge(UP, buff=1.5)
        input_chars = VGroup(*[Text(char, font_size=36) for char in input_str]).arrange(RIGHT, buff=0.4)
        input_chars.next_to(input_label, DOWN, buff=0.5)

        self.play(Write(input_label), Create(input_chars))
        self.wait(1)

        # DFA logic mapping for transitions and state objects
        dfa_transitions_map = {
            ("Q0", "a"): ("Q1", transition_q0_q1_a),
            ("Q0", "b"): ("Q0", transition_q0_loop_b),
            ("Q1", "a"): ("Q1", transition_q1_loop_a),
            ("Q1", "b"): ("Q0", transition_q1_q0_b),
        }
        state_objects_map = {"Q0": state_q0, "Q1": state_q1}
        accepting_states = {"Q1"}

        current_state_name = "Q0"
        # Highlight the initial state
        current_state_highlight = SurroundingRectangle(state_objects_map[current_state_name][0], color=YELLOW, buff=0.1, corner_radius=0.1)
        self.play(Create(current_state_highlight))
        self.wait(0.5)

        # Pointer for current input character
        char_pointer = Triangle(fill_opacity=1, color=YELLOW).scale(0.2).next_to(input_chars[0], DOWN, buff=0.2)
        self.play(Create(char_pointer))
        self.wait(0.5)

        processing_steps_title = Text("Processing Steps:", font_size=32).next_to(input_chars, DOWN, buff=1).align_to(input_label, LEFT)
        self.play(Write(processing_steps_title))
        self.wait(0.5)

        log_text_group = VGroup() # VGroup to hold all log lines

        for i, char_obj in enumerate(input_chars):
            char = input_str[i]
            
            # Highlight current character
            self.play(char_pointer.animate.next_to(char_obj, DOWN, buff=0.2), run_time=0.5)
            self.play(char_obj.animate.set_color(YELLOW), run_time=0.5)

            # Determine next state and the corresponding transition arrow VGroup
            next_state_name, transition_arrow_group = dfa_transitions_map[(current_state_name, char)]
            
            # Animate the transition arrow (the first element of the VGroup is the arrow/arc)
            self.play(Flash(transition_arrow_group[0], color=YELLOW, flash_radius=0.5), run_time=0.8)
            
            # Create and display a log line for the current step
            log_line = Text(f"Current: {current_state_name} | Read: '{char}' | Next: {next_state_name}", font_size=24)
            
            if not log_text_group.submobjects:
                log_line.next_to(processing_steps_title, DOWN, buff=0.3).align_to(processing_steps_title, LEFT)
            else:
                log_line.next_to(log_text_group.submobjects[-1], DOWN, buff=0.2).align_to(processing_steps_title, LEFT)
            
            self.play(Write(log_line))
            log_text_group.add(log_line)

            # Update the current state highlight to the new state
            self.play(
                current_state_highlight.animate.become(
                    SurroundingRectangle(state_objects_map[next_state_name][0], color=YELLOW, buff=0.1, corner_radius=0.1)
                ),
                char_obj.animate.set_color(WHITE), # Reset char color
                run_time=0.8
            )
            current_state_name = next_state_name
            self.wait(0.2)

        self.play(FadeOut(char_pointer))
        self.wait(1)

        # --- 6. Conclude (Accept/Reject) --- 
        result_text = Text("Result:", font_size=36).next_to(log_text_group, DOWN, buff=1).align_to(processing_steps_title, LEFT)
        self.play(Write(result_text))

        if current_state_name in accepting_states:
            final_status = Text(f"String '{input_str}' is ACCEPTED!", color=GREEN, font_size=40)
            self.play(Flash(current_state_highlight, color=GREEN, flash_radius=0.7, line_stroke_width=3))
        else:
            final_status = Text(f"String '{input_str}' is REJECTED.", color=RED, font_size=40)
            self.play(Flash(current_state_highlight, color=RED, flash_radius=0.7, line_stroke_width=3))
        
        final_status.next_to(result_text, DOWN, buff=0.5).align_to(result_text, LEFT)
        self.play(Write(final_status))
        self.wait(3)

        # Fade out all elements at the end
        self.play(FadeOut(title, dfa_diagram, input_label, input_chars, current_state_highlight, processing_steps_title, log_text_group, result_text, final_status))
        self.wait(1)
