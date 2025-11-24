import manim

class BubbleSortVisualization(manim.Scene):
    def construct(self):
        # --- Configuration --- #
        initial_array_values = [4, 2, 7, 1, 3]
        element_width = 1.2
        element_height = 1.2
        element_buff = 0.4
        default_color = manim.BLUE
        compare_color = manim.YELLOW
        swap_color = manim.RED
        sorted_color = manim.GREEN

        # --- Title and Introduction --- #
        title = manim.Text("Bubble Sort Visualization", font_size=50).to_edge(manim.UP)
        self.play(manim.Write(title))
        self.wait(0.5)

        intro_text = manim.Text(
            "Bubble Sort repeatedly steps through the list,"
            " compares adjacent elements and swaps them if they are in the wrong order.",
            font_size=28
        ).next_to(title, manim.DOWN, buff=0.8)
        self.play(manim.FadeIn(intro_text))
        self.wait(2)
        self.play(manim.FadeOut(intro_text))

        # --- Array Initialization --- #
        array_mobjects = []
        for value in initial_array_values:
            rect = manim.Rectangle(width=element_width, height=element_height, color=default_color, fill_opacity=0.5)
            text = manim.Text(str(value), font_size=36).move_to(rect.get_center())
            element_vg = manim.VGroup(rect, text)
            array_mobjects.append(element_vg)

        # Arrange the initial array elements
        array_group = manim.VGroup(*array_mobjects).arrange(manim.RIGHT, buff=element_buff).to_center()
        self.play(manim.Create(array_group))
        self.wait(1)

        # Keep a mutable list of the VGroups for easy access and swapping
        current_array_vgs = list(array_mobjects)
        # Also keep a Python list for logical comparison
        current_array_values = list(initial_array_values)

        # --- Sorting Process --- #
        n = len(current_array_vgs)

        pass_label = manim.Text("Pass: 0", font_size=30).to_edge(manim.LEFT).shift(manim.UP * 2)
        self.play(manim.FadeIn(pass_label))

        for i in range(n - 1):
            # Update pass label
            new_pass_label = manim.Text(f"Pass: {i + 1}", font_size=30).move_to(pass_label.get_center())
            self.play(manim.Transform(pass_label, new_pass_label))
            pass_label = new_pass_label # Update reference
            self.wait(0.5)

            for j in range(n - 1 - i):
                vg1 = current_array_vgs[j]
                vg2 = current_array_vgs[j + 1]

                # Highlight elements being compared
                self.play(
                    vg1[0].animate.set_color(compare_color),
                    vg2[0].animate.set_color(compare_color),
                    run_time=0.7
                )
                self.wait(0.3)

                if current_array_values[j] > current_array_values[j + 1]:
                    # Animate swap
                    self.play(
                        vg1[0].animate.set_color(swap_color),
                        vg2[0].animate.set_color(swap_color),
                        run_time=0.5
                    )
                    self.wait(0.2)

                    target_pos_vg1 = vg2.get_center()
                    target_pos_vg2 = vg1.get_center()

                    self.play(
                        vg1.animate.move_to(target_pos_vg1),
                        vg2.animate.move_to(target_pos_vg2),
                        run_time=1
                    )

                    # Update internal lists after animation
                    current_array_vgs[j], current_array_vgs[j + 1] = current_array_vgs[j + 1], current_array_vgs[j]
                    current_array_values[j], current_array_values[j + 1] = current_array_values[j + 1], current_array_values[j]

                    # Revert colors after swap
                    self.play(
                        current_array_vgs[j][0].animate.set_color(default_color),
                        current_array_vgs[j+1][0].animate.set_color(default_color),
                        run_time=0.5
                    )
                else:
                    # Revert colors if no swap
                    self.play(
                        vg1[0].animate.set_color(default_color),
                        vg2[0].animate.set_color(default_color),
                        run_time=0.5
                    )
                self.wait(0.2)

            # After each pass, the largest unsorted element is in its correct place
            # Mark the last element of the unsorted portion as sorted
            sorted_element_vg = current_array_vgs[n - 1 - i]
            self.play(sorted_element_vg[0].animate.set_color(sorted_color))
            self.wait(0.5)

        # Mark the first element as sorted after all passes (it's implicitly sorted)
        self.play(current_array_vgs[0][0].animate.set_color(sorted_color))
        self.wait(1)

        self.play(manim.FadeOut(pass_label))

        # --- Final State and Complexity --- #
        sorted_text = manim.Text("Array is Sorted!", font_size=40, color=sorted_color).next_to(array_group, manim.DOWN, buff=1.0)
        self.play(manim.FadeIn(sorted_text))
        self.wait(1)

        complexity_title = manim.Text("Time Complexity:", font_size=36).next_to(sorted_text, manim.DOWN, buff=0.8).align_to(sorted_text, manim.LEFT)
        time_complexity = manim.MathTex("O(n^2)", font_size=48, color=manim.YELLOW).next_to(complexity_title, manim.RIGHT, buff=0.5)

        space_complexity_title = manim.Text("Space Complexity:", font_size=36).next_to(complexity_title, manim.DOWN, buff=0.5).align_to(complexity_title, manim.LEFT)
        space_complexity = manim.MathTex("O(1)", font_size=48, color=manim.YELLOW).next_to(space_complexity_title, manim.RIGHT, buff=0.5)

        self.play(manim.FadeIn(complexity_title), manim.FadeIn(time_complexity))
        self.wait(1.5)
        self.play(manim.FadeIn(space_complexity_title), manim.FadeIn(space_complexity))
        self.wait(3)

        self.play(
            manim.FadeOut(title),
            manim.FadeOut(array_group),
            manim.FadeOut(sorted_text),
            manim.FadeOut(complexity_title),
            manim.FadeOut(time_complexity),
            manim.FadeOut(space_complexity_title),
            manim.FadeOut(space_complexity)
        )
        self.wait(1)
