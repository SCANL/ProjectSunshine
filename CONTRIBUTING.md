# IDEAL | CONTRIBUTING

## Commits

We have very precise rules over how our git commit messages can be formatted. This leads to more readable messages that are easy to follow when looking through the project history
We follow specs described by [Conventional Commits](https://www.conventionalcommits.org/).

The following is taken from https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines

### Commit Message Format

Each commit message consists of a `header`, a `body` and a `footer`. The header has a special format that includes a `type` and a `subject`:
Any line of the commit message cannot be longer 100 characters! This allows the message to be easier to read on GitHub as well as in various git tools.

```
<type>: <summary>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

### Header

The **header** is mandatory and the **scope** of the header must be omitted if the change is common among the packages, otherwise it's mandatory. Use the summary field to provide a succinct description of the change:

```
<type>(<scope>): <short summary>
  │       │             │
  │       │             └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │       │
  │       └─⫸ Commit Scope: server | app | desktop-app
  │
  └─⫸ Commit Type: build|ci|docs|feat|fix|perf|refactor|test
```

#### Summary

-   use the imperative, present tense: "change" not "changed" nor "changes"
-   don't capitalize the first letter
-   no dot (.) at the end

#### Type

Must be one of the following:

-   build: Changes that affect the build system or external dependencies
-   ci: Changes to our CI configuration files and scripts
-   docs: Documentation only changes
-   feat: A new feature
-   fix: A bug fix
-   perf: A code change that improves performance
-   refactor: A code change that neither fixes a bug nor adds a feature
-   style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
-   test: Adding missing tests or correcting existing tests

### Body

The **body** is mandatory for all commits except for those of type "docs". When the body is present it must be at least 20 characters long and must conform to the Commit Message Body format.
**Just as in the summary, use the imperative, present tense: "fix" not "fixed" nor "fixes".**
Explain the motivation for the change in the commit message body. This commit message should explain why you are making the change. You can include a comparison of the previous behavior with the new behavior in order to illustrate the impact of the change.

### Footer

The footer is optional. The footer should contain a [closing reference to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) if any. (e.g. Fixes #<issue-number>)

[Samples](https://github.com/angular/angular/commits/master)

## Branches

New branches must follow this format for their names: `<type>/<description>`

-   `type` refer to the one described in the Commits section.
-   `description` must be a word representing the changes happening in the branch, with less than 10 characters.
