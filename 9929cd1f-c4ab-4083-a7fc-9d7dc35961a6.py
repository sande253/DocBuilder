from manim import *

class TeslaSharesExplanation(Scene):
    def construct(self):
        # --- 0. Title --- (Approx. 2 seconds)
        title = Text("Tesla Shares in 30 Seconds", font_size=50, color=BLUE_C)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP).scale(0.7))

        # --- 1. Tesla Introduction --- (Approx. 5 seconds)
        tesla_logo_text = Text("TESLA", font_size=72, color=RED_E, weight=BOLD)
        tesla_inc_text = Text("Tesla Inc.", font_size=36, color=WHITE).next_to(tesla_logo_text, DOWN, buff=0.3)
        tesla_group = VGroup(tesla_logo_text, tesla_inc_text).move_to(ORIGIN)

        self.play(FadeIn(tesla_group))
        self.wait(1)

        # Brief description
        desc_text = Text("More than just cars...", font_size=30, color=YELLOW_C).next_to(tesla_group, DOWN, buff=0.8)
        self.play(Write(desc_text))
        self.wait(1)
        self.play(FadeOut(tesla_group, desc_text))

        # --- 2. Core Businesses --- (Approx. 4 seconds)
        # Using Rectangles with Text for visual elements representing business areas
        ev_rect = Rectangle(width=3, height=1.5, color=BLUE_A, fill_opacity=0.7)
        ev_text = Text("Electric Vehicles", font_size=24).move_to(ev_rect.get_center())
        ev_group = VGroup(ev_rect, ev_text)

        energy_rect = Rectangle(width=3, height=1.5, color=GREEN_A, fill_opacity=0.7)
        energy_text = Text("Energy Solutions", font_size=24).move_to(energy_rect.get_center())
        energy_group = VGroup(energy_rect, energy_text)

        ai_rect = Rectangle(width=3, height=1.5, color=PURPLE_A, fill_opacity=0.7)
        ai_text = Text("AI & Robotics", font_size=24).move_to(ai_rect.get_center())
        ai_group = VGroup(ai_rect, ai_text)

        business_groups = VGroup(ev_group, energy_group, ai_group).arrange(RIGHT, buff=0.8).next_to(title, DOWN, buff=1)

        self.play(FadeIn(business_groups, shift=UP))
        self.wait(2)
        self.play(FadeOut(business_groups))

        # --- 3. What is a Share? --- (Approx. 8 seconds)
        company_rect = Rectangle(width=6, height=4, color=BLUE_D, fill_opacity=0.8)
        company_label = Text("Tesla Inc. (Company)", font_size=36).move_to(company_rect.get_center())
        company_full_group = VGroup(company_rect, company_label).move_to(LEFT * 3)

        share_rect = Rectangle(width=2, height=1.5, color=GOLD_A, fill_opacity=0.9)
        share_label = Text("1 Share", font_size=28).move_to(share_rect.get_center())
        share_group = VGroup(share_rect, share_label)

        # Initially place share inside company to show it's a part
        share_group.move_to(company_full_group.get_center() + UP * 0.5 + RIGHT * 1)

        self.play(FadeIn(company_full_group))
        self.play(FadeIn(share_group))
        self.wait(1)

        # Explain share as a piece of ownership
        ownership_text = Text("A tiny piece of ownership.", font_size=30, color=YELLOW_C).next_to(company_full_group, RIGHT, buff=1)
        self.play(Write(ownership_text))
        self.wait(1)

        # Animate share moving out to emphasize it's a distinct asset
        self.play(share_group.animate.next_to(company_full_group, RIGHT, buff=0.5))
        self.wait(1)
        self.play(FadeOut(company_full_group, share_group, ownership_text))

        # --- 4. Why Invest? (Growth Potential) --- (Approx. 7 seconds)
        growth_title = Text("Why Invest?", font_size=40, color=BLUE_C).next_to(title, DOWN, buff=1)
        self.play(Write(growth_title))

        # Growth arrow and label
        growth_arrow = Arrow(start=LEFT * 2 + DOWN * 1, end=RIGHT * 2 + UP * 1, color=GREEN_E, buff=0).scale(1.5)
        growth_arrow_label = Text("Growth Potential", font_size=30).next_to(growth_arrow, UP, buff=0.5)
        growth_arrow_group = VGroup(growth_arrow, growth_arrow_label).move_to(ORIGIN + LEFT * 2)

        # Innovation and Market Leadership points
        innovation_text = Text("Innovation", font_size=30, color=WHITE).next_to(growth_arrow_group, RIGHT, buff=1)
        market_text = Text("Market Leadership", font_size=30, color=WHITE).next_to(innovation_text, DOWN, buff=0.5)
        
        self.play(FadeIn(growth_arrow_group, shift=DOWN))
        self.play(Write(innovation_text))
        self.play(Write(market_text))
        self.wait(2)
        self.play(FadeOut(growth_title, growth_arrow_group, innovation_text, market_text))

        # --- 5. Conclusion --- (Approx. 6.5 seconds)
        conclusion_text_1 = Text("Driven by future vision & innovation.", font_size=36, color=YELLOW_C).next_to(title, DOWN, buff=1)
        conclusion_text_2 = Text("Remember: Not financial advice!", font_size=30, color=RED_E).next_to(conclusion_text_1, DOWN, buff=0.8)
        
        self.play(Write(conclusion_text_1))
        self.wait(1.5)
        self.play(Write(conclusion_text_2))
        self.wait(2)
        self.play(FadeOut(conclusion_text_1, conclusion_text_2, title))
        self.wait(0.5)
