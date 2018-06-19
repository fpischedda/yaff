YAFF
===

Yet Another Failed Framework
----------------------------

From time to time I come back to game development mainly to create simple
experimental games and sometimes to partecipate to some contest such as PyWeek.

This little framework is the latest attempt to create a basic framework to help
me in the process of building simple 2D games; I don't expect it to grow in to
something professional or generally useful.

The framework is being developed with CPython 3.4 (now 3.6), if you want to
support other versions of python you have to do some work by yourself, and
please provide patches :)

Basic concepts
--------------

The framework exposes a couple of utility classes in order to get started
quickly with the game logic; the fundamental pieces are the Director class and
the Scene class:
- Director: handles scense and propagates events to the active Scene object
- Scene: abstracts a scene; receives user input events, and provide two
  fundamental callbacks on_draw and on_update

I think this is the very basic functionality that is needed in order to focus
to game logic.

Example
-------

In order to run the simplest example:
- create your virtual environment and install requirements with: pip install -r
  requirements.txt
- install yaff in the virtualenv with: python setup.py install
- run: python -m example_bouncing_balls.main

The other projects included in the repo are usually broken and may require
more work to run, for example pyweek20 requires more effort to run it.

License
-------

Copyright (c) 2015, Francesco Pischedda <francesco.pischedda@gmail.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. Neither the name of the <organization> nor the
   names of its contributors may be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY Francesco Pischedda ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Francesco Pischedda BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
