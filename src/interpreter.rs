use crate::ast::{Program, Statement, Expression, BinaryOperator};

pub struct Interpreter;

impl Interpreter {
    pub fn new() -> Self {
        Self
    }

    pub fn interpret(&self, program: Program) {
        for statement in program.statements {
            match statement {
                Statement::Puts(expr) => {
                    let value = self.evaluate_expression(&expr);
                    println!("{}", value);
                }
            }
        }
    }

    fn evaluate_expression(&self, expr: &Expression) -> f64 {
        match expr {
            Expression::Number(n) => *n,
            Expression::BinaryOp { left, op, right } => {
                let left_val = self.evaluate_expression(left);
                let right_val = self.evaluate_expression(right);
                match op {
                    BinaryOperator::Add => left_val + right_val,
                    BinaryOperator::Subtract => left_val - right_val,
                    BinaryOperator::Multiply => left_val * right_val,
                    BinaryOperator::Divide => left_val / right_val,
                }
            }
        }
    }
} 