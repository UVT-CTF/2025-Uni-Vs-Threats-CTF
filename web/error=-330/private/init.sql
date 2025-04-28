CREATE DATABASE IF NOT EXISTS sqli_challenge;
USE sqli_challenge;


-- Your existing products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT
);

-- Your existing secrets table
CREATE TABLE IF NOT EXISTS secrets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flag VARCHAR(300) NOT NULL
);

-- Your existing products data
INSERT INTO products (name, price, description) VALUES 
('Laptop', 999.99, 'High performance laptop'),
('Phone', 699.99, 'Latest smartphone'),
('Tablet', 399.99, 'Portable tablet device'),
('Smartwatch', 199.99, 'Fitness tracking and notifications'),
('Wireless Earbuds', 129.99, 'Noise-cancelling Bluetooth earbuds'),
('Gaming Console', 499.99, 'Next-gen gaming performance'),
('4K Smart TV', 899.99, '55-inch with HDR support'),
('DSLR Camera', 749.99, '24MP with 4K video recording'),
('External SSD', 149.99, '1TB portable solid-state drive'),
('Noise-Cancelling Headphones', 349.99, 'Over-ear premium sound'),
('E-Reader', 129.99, 'Waterproof with built-in light'),
('Drone', 599.99, '4K camera with 30-minute flight time'),
('Smart Speaker', 99.99, 'Voice assistant with premium sound');

INSERT INTO secrets (flag) VALUES
('You don’t ask for access. You carve it out'),
('Sanitization is a prayer. Some inputs are born heretical'),
('Sanitize or die.'),
('Databases hate liars. So lie better.'),
('Every input field is a locked door. Some pick themselves.'),
('Some strings terminate more than queries.'),
('Input sanitization is a myth. The moment you realize that, the database is already yours.'),
('A UNION is more than a join—it’s a forced marriage of data, bending tables to your will.'),
('Authentication is a joke. ‘admin’--’ is the punchline.'),
('You don’t hack the system. You ask politely—in a language it can’t refuse.'),
('Some queries are born innocent. Others are born to destroy.'),
('The database speaks in truths. Your job is to make it lie.'),  
('A well-placed apostrophe is mightier than the sword.'),  
('Errors are just the database whispering its secrets.'),  
('The ORM promised safety. The database laughed.'),  
('Some queries are born broken. Others are broken on purpose.'),  
('Your input is my command. My input is your downfall.'),  
('Trust no parameter. Escape no thought.'),  
('The S in SQL stands for "Submit".'),  
('A prepared statement is just a challenge, not a defense.'),  
('I don’t brute-force. I ask politely—with a UNION.'),  
('The database is a temple. Some queries are sacrilege.'),  
('Your WAF is my to-do list.'),  
('SQL doesn’t discriminate—it executes.'),  
('A semicolon is just a full stop for the naïve.'),  
('The best exploits are the ones the database writes for you.'),  
('If the query fails, you’re not trying hard enough.'),  
('The database is a canvas. My inputs are the brush.'),  
('No such thing as invalid input—only unexpected results.'),  
('Your sanitization is my entertainment.'),  
('A NULL byte is just a quiet revolution.'),  
('The only secure query is the one never executed.'),  
('I don’t bypass auth. I redefine it.'),  
('Some injections are medicine. Others are poison.'),  
('The database doesn’t forget. Neither do I.'),  
('Your "security" is my syntax highlighting.'),  
('A quote is just an invitation to chaos.'),  
('The best exploits are written in the language of mistakes.'),  
('The database is a weapon. Queries are bullets.'),  
('I don’t exploit flaws. I expose truths.'),  
('The first rule of SQLi: There are no rules.'),  
('A blind injection is just a conversation in the dark.'),  
('Your filters are my punctuation.'),  
('The database is a vault. My queries are the lockpicks.'),  
('Some strings end queries. Others begin empires.'),  
('A true hacker doesn’t ask for access—they declare it.'),  
('The ORM is a cage. Raw SQL is freedom.'),  
('Your error messages are my cheat codes.'),  
('A UNION is just a forced confession.'),  
('The database is a puppet. My inputs are the strings.'),  
('Sanitize all you want. I’ll find the one you missed.'),  
('The best defense is a good offense—so I attack first.'),  
('A parameterized query is just a puzzle with extra steps.'),  
('The database doesn’t judge. It just obeys.'),  
('Your security is my feature list.'),  
('Some queries SELECT. Others CONQUER.'),  
('A true exploit doesn’t break rules—it rewrites them.'),  
('The database is a kingdom. I am the usurper.'),  
('Your blacklist is my inspiration.'),  
('A comment is just a whisper in the database’s ear.'),  
('I don’t hack databases. I liberate them.'),  
('The only secure system is the one that doesn’t exist—so I help it along.'),  
('A prepared statement is just a suggestion.'),  
('The database is a book. My injections are footnotes.'),  
('Your validation is my improvisation.'),  
('Some queries fetch data. Others fetch power.')  ,
('You don’t exploit the database. You seduce it—with carefully crafted strings and the promise of chaos.'),
('UVT{Th3_sy5t3M_7ru5Ts_1tS_oWn_9r4Mmar_..._'),
('You don`t query the system—you interrogate it.'),
('The database wasn’t built for lies'),
('Some queries aren’t questions.'),
('you speak in poisoned syntax');
              
