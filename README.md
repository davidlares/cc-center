# Command and Control Center

The following is a script that complements the [TCP Reverse Shell Script](https://gitlab.com/davidlares/tcp-reverse-shell) project, which lets you manage multiple client (victim) connections using low-level TCP sockets implementations with the help of `Threads` module, storing its IP and target arrays for quick access and for managing sessions along an internal `Botnet` (local `Botnet`)

This `cc.py` file lets you listen for any incoming socket connection and perform a TCP reverse shell "attack" for any particular (target IP) stored in the local array value

## Setting up the C&C

Check the `requirements.txt`, its recommended to use a `virtualenv` setup for installing dependencies and for an isolated environment.

## Usage

Just: `python cc.py`

Then:

  - Showing the list of targets with the `CC: target`
  - Accessing to any particular session (0-index), like: `session 0`

## Credits

  [David E Lares](https://twitter.com/davidlares3)

## License

  [MIT](https://opensource.org/licenses/MIT)
