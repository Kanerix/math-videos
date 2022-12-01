from manim import *
import math


class NewtonRaphsonIntro(Scene):
	def construct(self):
		x_range = ValueTracker([1, 10, 1])
		axes = always_redraw(lambda: Axes(
			x_range=x_range.get_value(), y_range=[0, 10, 1]))
		graph = always_redraw(lambda: axes.plot(lambda x: x**2, color=BLUE))

		self.play(Create(axes), Create(graph))
		self.play(x_range.animate.set([1, 3, 1]))


class NewtonRaphsonProof(Scene):
	def construct(self):
		def func(x): return x - math.cos(x)
		def func_deriv(x): return 1 + math.sin(x)

		axes = Axes(
			x_range=[-1, 10, 1],
			y_range=[-1, 7, 1],
		).scale(0.85)
		axes.to_edge(UL)
		graph = axes.plot(func, color=BLUE)
		self.play(Create(axes))
		self.play(Create(graph))
		self.wait()

		zero_point_dot = Dot(axes.c2p(0.739, 0))
		zero_point_label = MathTex("x")
		zero_point_label.next_to(zero_point_dot, DOWN)
		self.play(Create(zero_point_dot), Write(zero_point_label))
		self.wait()

		starting_number = 6.4
		drawing_queue = []

		for i in range(3):
			number = starting_number if i == 0 else drawing_queue[i-1]["x_value"]

			graph_dot = Dot(axes.c2p(number, func(number)))
			x_axes_dot = Dot(axes.c2p(number, 0))
			x_axes_label = MathTex(f"x_{i}").next_to(x_axes_dot, DOWN)
			v_line = DashedLine(
				graph_dot.get_bottom(),
				x_axes_dot.get_top(),
				color=RED
			)

			def tangent(x): return (func_deriv(number) *
									(x - number) + func(number))
			graph_tangent = axes.plot(tangent, color=GREEN)

			def newton_raphsons(x): return (x - func(x) / func_deriv(x))
			tangent_x_interceptor = Dot(
				axes.c2p(newton_raphsons(number), 0)
			)
			tangent_x_interceptor_label = MathTex(
				f"x_{i+1}").next_to(tangent_x_interceptor, DOWN)

			drawing_queue.append({
				"x_value": newton_raphsons(number),
				"graph_dot": graph_dot,
				"x_axes_dot": x_axes_dot,
				"x_axes_label": x_axes_label,
				"v_line": v_line,
				"graph_tangent": graph_tangent,
				"tangent_x_interceptor_dot": tangent_x_interceptor,
				"tangent_x_interceptor_label": tangent_x_interceptor_label,
			})

		self.play(Create(drawing_queue[0]["graph_dot"]))
		self.play(Create(drawing_queue[0]["v_line"]))
		self.play(
			Create(drawing_queue[0]["x_axes_dot"]),
			Write(drawing_queue[0]["x_axes_label"])
		)
		self.wait()

		self.play(Create(drawing_queue[0]["graph_tangent"]))
		self.play(
			Create(drawing_queue[0]["tangent_x_interceptor_dot"]),
			Write(drawing_queue[0]["tangent_x_interceptor_label"])
		)

		tangent_formula = MathTex(
			"y = {f'(x_0)} (x - x_0) + {f(x_0)}",
		).shift(2.75*DOWN)
		self.play(Write(tangent_formula))
		self.wait()

		tangent_formula_rewritten = MathTex(
			"0 = {f'(x_0)} (x - x_0) + {f(x_0)}",
			substrings_to_isolate=["{f(x_0)}", "{f'(x_0)}", "x_0", "x"]
		).shift(2.75*DOWN)
		self.play(TransformMatchingTex(
			tangent_formula, tangent_formula_rewritten))
		self.wait()

		tangent_formula_isolate_parentheses = MathTex(
			"(x - x_0) = - { {f(x_0)} \\over {f'(x_0)} }",
			substrings_to_isolate=["{f(x_0)}", "{f'(x_0)}", "x_0", "x"]
		).shift(2.75*DOWN)
		self.play(TransformMatchingTex(
			tangent_formula_rewritten, tangent_formula_isolate_parentheses))
		self.wait()

		tangent_formula_isolate_x = MathTex(
			"x = x_0 -{ {f(x_0)} \\over {f'(x_0)} }",
			substrings_to_isolate=["{f(x_0)}", "{f'(x_0)}", "x_0", "x"]
		).shift(2.75*DOWN)
		self.play(TransformMatchingTex(
			tangent_formula_isolate_parentheses, tangent_formula_isolate_x))
		self.wait()

		newton_raphsons_fomula = MathTex(
			"x_{n+1} = x_{n} - { {f(x_{n})} \\over {f'(x_{n})} }",
			substrings_to_isolate=["{f(x_{n})}", "{f'(x_{n})}", "x_{n+1}", "x_{n}"]
		).shift(2.75*DOWN)
		self.play(TransformMatchingTex(
			tangent_formula_isolate_x, newton_raphsons_fomula))
		self.wait()

		self.play(Uncreate(zero_point_dot), Unwrite(zero_point_label))
		self.wait()

		self.play(Uncreate(drawing_queue[0]["graph_tangent"]))
		self.play(Uncreate(drawing_queue[0]["graph_dot"]))
		self.play(Uncreate(drawing_queue[0]["v_line"]))
		self.play(
			Uncreate(drawing_queue[0]["x_axes_dot"]),
			Unwrite(drawing_queue[0]["x_axes_label"]),
		)
		self.wait()

		for i in range(1, len(drawing_queue)):
			self.play(Create(drawing_queue[i]["graph_dot"]))
			self.play(Create(drawing_queue[i]["v_line"]))
			self.play(Create(drawing_queue[i]["graph_tangent"]))
			self.play(
				Create(drawing_queue[i]["tangent_x_interceptor_dot"]),
				Write(drawing_queue[i]["tangent_x_interceptor_label"])
			)
			self.wait()

			self.play(Uncreate(drawing_queue[i]["graph_tangent"]))
			self.play(Uncreate(drawing_queue[i]["graph_dot"]))
			self.play(Uncreate(drawing_queue[i]["v_line"]))
			self.play(
				Uncreate(drawing_queue[i-1]["tangent_x_interceptor_dot"]),
				Unwrite(drawing_queue[i-1]["tangent_x_interceptor_label"])
			)

		self.wait()