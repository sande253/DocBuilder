
    from manim import *

    class AutomataDemoRobust(Scene):
    

        def construct(self):
            # ---------- Config ----------
            states = {}
            state_positions = {
                "q0": LEFT * 4,
                "q1": ORIGIN,
                "q2": RIGHT * 4,
            }

            # ---------- Create states ----------
            for name, pos in state_positions.items():
                circle = Circle(radius=0.8)
                label = Text(name).move_to(circle.get_center())
                states[name] = VGroup(circle, label).move_to(pos)

            # Initial and accepting state styling
            states["q0"][0].set_color(BLUE)  # initial state
            states["q2"][0].set_color(GREEN)  # accepting state
            states["q2"][0].set_stroke(width=4)

            # Display states
            for st in states.values():
                self.play(FadeIn(st))
            self.wait(0.5)

            # ---------- Define transitions ----------
            transitions = []

            # Each transition: (from_state, to_state, label)
            transition_data = [
                ("q0", "q1", "a"),
                ("q1", "q2", "b"),
                ("q1", "q1", "a"),  # self-loop
                ("q2", "q2", "b"),  # self-loop
            ]

            def make_transition(from_state, to_state, label_text):
                start = states[from_state].get_center()
                end = states[to_state].get_center()

                if from_state == to_state:
                    # self-loop: draw small Arc above state
                    loop = Arc(
                        radius=0.7,
                        start_angle=-PI/2,
                        angle=2*PI,
                        arc_center=start + UP*0.8
                    )
                    label = Text(label_text).scale(0.6).next_to(loop, UP)
                    return VGroup(loop, label)
                else:
                    vec = end - start
                    direction = vec / np.linalg.norm(vec)
                    start_adj = start + direction * 0.8
                    end_adj = end - direction * 0.8
                    arrow = Arrow(start_adj, end_adj, buff=0)
                    label = Text(label_text).scale(0.6)
                    label.move_to((start_adj + end_adj)/2 + UP*0.3)
                    return VGroup(arrow, label)

            # Create transition objects
            for from_s, to_s, lab in transition_data:
                t = make_transition(from_s, to_s, lab)
                transitions.append((from_s, to_s, lab, t))
                self.play(Create(t))
            self.wait(0.5)

            # ---------- Input string ----------
            input_string = "aab"
            path = ["q0", "q1", "q1", "q2"]  # precomputed path for demo
            input_text = Tex(f"Input: {input_string}").to_corner(UP+LEFT)
            self.play(FadeIn(input_text))
            self.wait(0.3)

            # ---------- Animate processing ----------
            for i in range(len(input_string)):
                from_state = path[i]
                to_state = path[i+1]
                char = input_string[i]

                # Highlight transition arrow (or self-loop)
                for f, t, label, tg in transitions:
                    if f == from_state and t == to_state and label == char:
                        highlight = tg[0].copy().set_color(YELLOW)
                        self.play(Create(highlight), run_time=0.5)
                        break

                # Highlight next state
                self.play(states[to_state][0].animate.set_fill(YELLOW, opacity=0.3), run_time=0.3)
                self.wait(0.3)

            # ---------- Final acceptance ----------
            final_state = path[-1]
            self.play(states[final_state][0].animate.set_fill(GREEN, opacity=0.5))
            self.wait(0.8)

            # Display result text
            result_text = Tex(f"Final state: {final_state} → Accepted").to_edge(DOWN)
            self.play(FadeIn(result_text))
            self.wait(1.2)


    