# Documentation-Driven Development

The philosophy behind Documentation-Driven Development is a simple: **from the perspective of a user, if a feature is not documented, then it doesn't exist, and if a feature is documented incorrectly, then it's broken.**

- Document the feature *first*. Figure out how you're going to describe the feature to users; if it's not documented, it doesn't exist. Documentation is the best way to define a feature in a user's eyes.
- Whenever possible, documentation should be reviewed by users (community or Spark Elite) before any development begins.
- Once documentation has been written, development should commence, and test-driven development is preferred.
- Unit tests should be written that test the features as described by the documentation. If the functionality ever comes out of alignment with the documentation, tests should fail.
- When a feature is being modified, it should be modified documentation-first.
- When documentation is modified, so should be the tests.
- Documentation and software should both be versioned, and versions should match, so someone working with old versions of software should be able to find the proper documentation.

So, the preferred order of operations for new features:
- Write documentation
- Get feedback on documentation
- Test-driven development (where tests align with documentation)
- Push features to staging
- Functional testing on staging, as necessary
- Deliver feature
- Publish documentation
- Increment versions

## Research Software Engineering
Research software engineering (RSE) best practices emphasize readability, maintainability, reproducibility, and collaboration through techniques like using version control (Git), writing clean and modular code, comprehensive testing and documentation, engaging in code reviews, and managing development with a structured life cycle.

### Code & Design Practices
- Write Readable and Maintainable Code: Focus on clarity, use meaningful names for variables and functions, and follow language-specific style guides. 
- Design for Modularity: Break down software into small, reusable components with specific functions to enhance maintainability and scalability. 
- Embrace DRY (Don't Repeat Yourself): Avoid duplicating code to reduce errors and improve consistency. 
- Follow Software Engineering Principles: Principles like modularity, abstraction, encapsulation, and separation of concerns are fundamental for robust and scalable systems. 

### Development & Collaboration
- Use Version Control: Employ systems like Git to track changes, collaborate effectively, and revert to previous versions if needed. 
- Implement Automated Testing: Regularly test your code to catch bugs early and ensure reliability. 
- Conduct Code Reviews: Have agents to review your code to improve quality, share knowledge, and catch errors. 
- Plan with a Life Cycle: Use a phased approach to manage the development process, from planning and design to deployment and maintenance. 

### Documentation & Reproducibility
- Document Thoroughly: Write clear documentation, including code comments and README files, to explain how the software works and how to use it. 
- Ensure Reproducibility: Strive for outputs that can be reproduced by others by clearly documenting the code and its dependencies. 
- Use Meaningful Names: Choose names for variables, functions, and other code elements that clearly convey their purpose, saving time and effort. 

### Project Management & User Engagement
- Plan Before Coding: Invest time in planning to ensure a clear vision for the project before writing code. 
- Manage Environments: Keep your development environments organized and consistent. 
- Involve Users Early: Get human feedback from users as early as possible in the development process to ensure the software meets their needs. 
- Plan for Long-Term Maintenance: Think about the software's lifespan beyond the initial development to ensure it can be supported and updated over time.
