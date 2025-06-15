mod ast;
mod parser;
mod interpreter;

use std::fs;
use clap::Parser as ClapParser;
use anyhow::Result;

#[derive(ClapParser)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// The source file to run
    file: String,
}

fn main() -> Result<()> {
    let args = Args::parse();
    let source = fs::read_to_string(&args.file)?;
    
    let program = parser::parse(&source)?;
    let interpreter = interpreter::Interpreter::new();
    interpreter.interpret(program);
    
    Ok(())
}
