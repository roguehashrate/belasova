#[derive(Debug, Clone)]
pub enum Expression {
    Number(f64),
    BinaryOp {
        left: Box<Expression>,
        op: BinaryOperator,
        right: Box<Expression>,
    },
}

#[derive(Debug, Clone)]
pub enum BinaryOperator {
    Add,
    Subtract,
    Multiply,
    Divide,
}

#[derive(Debug, Clone)]
pub enum Statement {
    Puts(Expression),
}

#[derive(Debug, Clone)]
pub struct Program {
    pub statements: Vec<Statement>,
} 