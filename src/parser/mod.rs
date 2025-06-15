use pest::Parser;
use pest_derive::Parser;
use crate::ast::{Program, Statement, Expression, BinaryOperator};

#[derive(Parser)]
#[grammar = "parser/grammar.pest"]
pub struct BelasovaParser;

pub fn parse(source: &str) -> Result<Program, pest::error::Error<Rule>> {
    let pairs = BelasovaParser::parse(Rule::program, source)?;
    let mut statements = Vec::new();

    for pair in pairs {
        match pair.as_rule() {
            Rule::program => {
                for statement in pair.into_inner() {
                    if statement.as_rule() == Rule::statement {
                        for puts_stmt in statement.into_inner() {
                            if puts_stmt.as_rule() == Rule::puts_stmt {
                                let mut inner = puts_stmt.into_inner();
                                inner.next(); // Skip "puts"
                                if let Some(expr) = inner.next() {
                                    statements.push(Statement::Puts(parse_expression(expr)));
                                }
                            }
                        }
                    }
                }
            }
            _ => {}
        }
    }

    Ok(Program { statements })
}

fn parse_expression(pair: pest::iterators::Pair<Rule>) -> Expression {
    match pair.as_rule() {
        Rule::expression => {
            let mut pairs = pair.into_inner();
            let mut expr = parse_term(pairs.next().unwrap());
            
            while let Some(op) = pairs.next() {
                let right = parse_term(pairs.next().unwrap());
                expr = Expression::BinaryOp {
                    left: Box::new(expr),
                    op: match op.as_str() {
                        "+" => BinaryOperator::Add,
                        "-" => BinaryOperator::Subtract,
                        _ => unreachable!(),
                    },
                    right: Box::new(right),
                };
            }
            expr
        }
        _ => unreachable!(),
    }
}

fn parse_term(pair: pest::iterators::Pair<Rule>) -> Expression {
    match pair.as_rule() {
        Rule::term => {
            let mut pairs = pair.into_inner();
            let mut expr = parse_factor(pairs.next().unwrap());
            
            while let Some(op) = pairs.next() {
                let right = parse_factor(pairs.next().unwrap());
                expr = Expression::BinaryOp {
                    left: Box::new(expr),
                    op: match op.as_str() {
                        "*" => BinaryOperator::Multiply,
                        "/" => BinaryOperator::Divide,
                        _ => unreachable!(),
                    },
                    right: Box::new(right),
                };
            }
            expr
        }
        _ => unreachable!(),
    }
}

fn parse_factor(pair: pest::iterators::Pair<Rule>) -> Expression {
    match pair.as_rule() {
        Rule::number => {
            let num = pair.as_str().parse::<f64>().unwrap();
            Expression::Number(num)
        }
        Rule::expression => parse_expression(pair),
        _ => unreachable!(),
    }
} 