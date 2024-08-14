node
========

Installs a `node` binary into your project, which because `npm` runs scripts with the local `./node_modules/.bin` in the `PATH` ahead of the system copy means you can have a local version of node that is different than your system's, and manage node as a normal dependency.

Warning: don't install this globally with npm 2. `npm@2` immediately removes node, then can't run the scripts that make this work.

Use
---

```
npm i node@lts
```

Use with `npx`
--------------

```
npx node@4 myscript.js
```

This will run `myscript.js` with the latest version of node from the v4 major.

Using the shell auto-fallback of npx, you can even do it like so:


```
node@4 myscript.js
```

Thanks
------

Major thanks to Kat Marchán for late-night problem solving, and to CJ Silverio and Maciej Małecki for egging me on way back when I had the idea to package node up this way. It does turn out if you ask "why _not_?!" once in a while something fun happens.
