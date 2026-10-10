"""Writing for Video with AI: page content. Edit the HTML here, then run build.py."""
from common import page, render, BYLINE

BODY = f"""

<section class="page">
  <header>
    <div>
      <div class="kicker">Video playbook</div>
      <h1>Writing for Video with AI</h1>
      <p class="sub">For a 30 second feed clip, a 10 minute explainer or a full course. Works in Claude, ChatGPT or any assistant you like.</p>
    </div>
    {BYLINE}
  </header>

  <section class="stats">
    <div class="stat"><div class="v">150</div><div class="l"><b>Courses</b> on LinkedIn Learning.</div></div>
    <div class="stat"><div class="v">3M+</div><div class="l"><b>Learners</b> across those courses.</div></div>
    <div class="stat"><div class="v">3x</div><div class="l"><b>Output, same hours.</b> One big course a month became 2 to 3 short videos a week.</div></div>
    <div class="stat"><div class="v">~200K</div><div class="l"><b>Learners on AI Trends,</b> close to 10K bookmarks. It ships while the topic is live.</div></div>
  </section>

  <section class="block">
    <h2>Build your writing files <span class="tag">Living documents</span></h2>
    <p class="lead">Give the AI a clear picture of you, your audience and your formats. Four small files do it, and they get better every time you write. My free <a href="https://github.com/planetoftheweb/writing-companion">Writing Companion</a> skill walks you through building them.</p>
    <div class="filerow">
      <div class="card file"><div class="scope">Everything you write</div><div class="nm">Soul file</div><p>Your voice. How you sound and what you believe: tone, energy, point of view, rhythm, humor.</p><p class="eg"><b>Mine:</b> warm, direct, short sentences, and sure these tools make you superhuman.</p><p class="eg"><b>Starter:</b> <a href="https://github.com/planetoftheweb/writing-companion/blob/main/skills/writing-companion/assets/guidance/voice-options.md">voice and rules</a></p></div>
      <div class="card file"><div class="scope">Everything you write</div><div class="nm">Rules file</div><p>Your do's and don'ts: words to avoid, punctuation, terms, links, hashtags and how you end.</p><p class="eg"><b>Mine:</b> no em dashes, no hype, no hashtags.</p></div>
      <div class="card file hi"><div class="scope">One per series</div><div class="nm">POV statement</div><p>The promise: who it is for, the question every episode answers and what viewers can do after. Mine for AI Trends:</p>
        <div class="chips"><span>Respect their time</span><span>Filter ruthlessly</span><span>Real demos</span><span>No algorithm chasing</span><span>Positive outlook</span></div><p class="eg" style="margin-top:4pt;"><b>Starter:</b> <a href="https://github.com/planetoftheweb/writing-companion/blob/main/skills/writing-companion/assets/guidance/series.md">series promise template</a></p></div>
      <div class="card file"><div class="scope">One per format</div><div class="nm">Format files</div><p>A template plus short writing instructions for each kind of piece. One series can use several.</p>
        <div class="chips"><span>Feed clip</span><span>Long video</span><span>Post</span><span>Newsletter</span></div><p class="eg" style="margin-top:4pt;"><b>Starters:</b> <a href="https://github.com/planetoftheweb/writing-companion/tree/main/skills/writing-companion/assets/content-types">scripts, posts and more</a></p></div>
    </div>
    <div class="arrows"><span>&#9660;</span><span>&#9660;</span><span>&#9660;</span><span>&#9660;</span></div>
    <div class="flowbar"><div class="piece">Every piece you write pulls from all four <span>feed clip, explainer, course, post</span></div><div class="cycle">&#8635; Improve them after every piece</div></div>
  </section>

  <section class="block two">
    <div>
      <h2>Keep them alive <span class="tag">They are never done</span></h2>
      <ol class="rules">
        <li><b>Start from real work.</b> Give the AI 2 or 3 pieces that sound like you. Ask it to describe your voice, then correct what it gets wrong. No samples yet? Have it ask you a few questions and write two different openings so you can pick.</li>
        <li><b>Keep only what you confirm.</b> The AI's guesses stay out of your files until you say yes.</li>
        <li><b>Update after every piece.</b> Ask the AI to compare its draft with your final and suggest up to three lessons. Keep the lasting ones.</li>
        <li><b>Put each lesson in the right file.</b> A habit goes in your soul or rules file. A series need goes in the POV statement. A fixed fact stays with that piece.</li>
        <li><b>Save the old version.</b> If a change makes your drafts worse, roll it back.</li>
      </ol>
    </div>
    <div>
      <h2>Put them to work <span class="tag">Pick one setup</span></h2>
      <div class="opt"><h3>Just starting? Paste them in</h3><p>Paste your files at the top of a new chat. It works anywhere, but you repeat it every time. No files yet? Try the <a href="https://github.com/planetoftheweb/writing-companion/blob/main/docs/prompts.md">prompt series</a>.</p></div>
      <div class="opt hi"><span class="badge">Best for recurring work</span><h3>A Project with a custom instruction</h3><p>Create a Claude Project, or a ChatGPT Project. Add your files as project knowledge. Then paste the custom instruction below so every chat checks them.</p></div>
      <div class="opt"><h3>Everywhere: a skill</h3><p>Package your files as a skill. It loads whenever you write, in any chat. Claude supports skills, and so do some ChatGPT plans. Start with <a href="https://github.com/planetoftheweb/writing-companion">Writing Companion</a>, free on GitHub.</p></div>
    </div>
  </section>

  <div class="prompt"><div class="pl">Custom instruction for your Project</div><div class="pt">Before you write anything, read my soul file, my rules file and the POV statement for this series. Write in my voice and keep the series promise. Before you show me a draft, check it against all three and fix what does not match. Ask me no more than three questions at a time. Never invent experiences, results, quotes or sources. After I edit a draft, suggest up to three changes to my files and say which file each belongs in.</div></div>

  <footer>Sources: course, learner, output and AI Trends figures from my own work. Starters and prompts: <a href="https://github.com/planetoftheweb/writing-companion">github.com/planetoftheweb/writing-companion</a></footer>
</section>

<section class="page">
  <div class="runhead"><span>Writing for Video with AI</span><span>Page 2</span></div>

  <section class="block">
    <h2>Prompts to get started <span class="tag">Copy, paste, fill the brackets</span></h2>
    <p class="lead">Short versions from my Writing Companion skill. The <a href="https://github.com/planetoftheweb/writing-companion/blob/main/docs/prompts.md">full prompt series</a> has ten, from finding your voice to saving your profile.</p>
    <div class="two" style="gap: 7pt 12pt;">
      <div class="prompt"><div class="pl">1. Find my voice</div><div class="pt">Here are three things I wrote that sound like me. Describe my voice: tone, energy, point of view, rhythm and humor. Separate what you can see from what you are guessing. Then write two short openings about [topic] in that voice so I can pick one.</div></div>
      <div class="prompt"><div class="pl">2. Write my POV statement</div><div class="pt">Help me write the promise for my series [name]. Cover who it is for, the question every episode answers, what viewers can do after watching, and what is out of bounds. Ask me no more than three questions first.</div></div>
      <div class="prompt"><div class="pl">3. Draft a script</div><div class="pt">Using my soul file, rules file and POV statement, write a [60 second] script for [platform] about [topic]. Write for the ear, one idea at a time. Note what is on screen for each line. In demos, never predict what the AI will answer.</div></div>
      <div class="prompt"><div class="pl">4. Learn from my edits</div><div class="pt">Compare your draft with my final version. Suggest up to three lasting changes to my files. For each one, show the edit you saw and say which file it belongs in, or whether it only applies to this piece.</div></div>
      <div class="prompt"><div class="pl">5. Make a companion post</div><div class="pt">Turn this script into a LinkedIn post for the video. Reflect what is in it, tease what viewers will see, and give one useful takeaway that stands on its own. Do not reuse the script's opening. Follow my rules file.</div></div>
      <div class="prompt"><div class="pl">6. Set up a new format</div><div class="pt">Help me create a reusable format for [feed clip, newsletter, post]. Give me a template for the structure and separate writing instructions. Test them on a short real piece before I save them.</div></div>
    </div>
  </section>

  <section class="block">
    <h2>Let AI do the heavy lifting <span class="tag">Research, options, rewrites, visuals</span></h2>
    <div class="three">
      <div class="card"><h3>Research</h3><p>Give it your links and notes. Ask for a short brief with the facts, dates and sources you need, plus what still needs checking.</p></div>
      <div class="card"><h3>Options</h3><p>Select a paragraph and ask for 5 versions in your voice. For titles, ask for 10. Pick one, or mix two.</p></div>
      <div class="card"><h3>Rewrite one part</h3><p>Highlight a line and say what to change, like "make this transition about how we got here." It rewrites only that part, in your voice.</p></div>
      <div class="card"><h3>Visual ideas</h3><p>Ask what to show for a section. You get options like a table, a timeline, cards or a chart, plus prompts for illustrations.</p></div>
      <div class="card"><h3>Learn from your edits</h3><p>After you edit, ask which lessons to keep and where each belongs: your soul file for every piece, or the series file for just that series.</p></div>
      <div class="card"><h3>Format for recording</h3><p>Keep spoken lines, on-screen visuals and recording notes apart, so a teleprompter shows only the words you say.</p></div>
    </div>
  </section>

  <section class="block">
    <h2>Check every draft against your files <span class="tag">Your contract with the viewer</span></h2>
    <table class="checks-t">
      <thead><tr><th>Check</th><th>What it asks</th><th>Checks against</th></tr></thead>
      <tbody>
        <tr><td><b>Voice</b></td><td>Does it sound like me: rhythm, tone and word choice?</td><td>Soul file</td></tr>
        <tr><td><b>Rules</b></td><td>Any banned words, punctuation or formats?</td><td>Rules file</td></tr>
        <tr class="hi"><td><b>Promise</b></td><td>Does it deliver what this series promises the viewer?</td><td>POV statement</td></tr>
        <tr><td><b>Evidence</b></td><td>Is every claim supported? What needs my confirmation?</td><td>Your sources</td></tr>
        <tr><td><b>Specific</b></td><td>Could this line belong to anyone? Make it specific or cut it.</td><td>Your experience</td></tr>
        <tr><td><b>Read aloud</b></td><td>One speaking beat per paragraph, about 25 to 60 words.</td><td>Format file</td></tr>
        <tr><td><b>AI demos</b></td><td>Does it assume what an AI will answer? Keep the demo open.</td><td>The live recording</td></tr>
        <tr><td><b>Performance</b></td><td>Does it match what has worked with your audience before?</td><td>Your analytics rubric</td></tr>
      </tbody>
    </table>
    <div class="prompt" style="margin-top:7pt;"><div class="pl">Copy this check prompt</div><div class="pt">Check this draft against my soul file, rules file, POV statement and performance rubric. Then check evidence, specific detail and read-aloud pacing. For each problem, quote the line, name the check it fails and suggest a fix in my voice. Leave the lines that pass alone.</div></div>
  </section>

  <footer>Prompts adapted from <a href="https://github.com/planetoftheweb/writing-companion">Writing Companion</a> (github.com/planetoftheweb/writing-companion). The helpers and checks match the AI tools I use in my own writing app.</footer>
</section>

<section class="page">
  <div class="runhead"><span>Writing for Video with AI</span><span>Page 3</span></div>

  <section class="block">
    <h2>Write for the ear and the screen <span class="tag">Tips that hold up on camera</span></h2>
    <div class="two">
      <ol class="rules">
        <li><b>Write with visuals in mind.</b> Attention spans are short. Next to each paragraph, note what is on screen: a demo, a chart or a screenshot. If nothing fits, that part is probably too long.</li>
        <li><b>One point per video.</b> A feed clip makes one point. A longer video walks through one task. Two points? Make two videos.</li>
        <li><b>Check the length before you record.</b> Most people speak about 150 words a minute. A one minute clip is about 150 words. A 10 minute video is about 1,500.</li>
        <li><b>Open with the payoff.</b> Skip the welcome and the agenda. Start with what people will be able to do, then get to the demo fast.</li>
        <li><b>Talk to one person.</b> Use "you," contractions and short sentences, the way you would explain it to a friend.</li>
      </ol>
      <ol class="rules" style="counter-reset: n 5;">
        <li><b>Let the screen do the showing.</b> People can see what you click. Use your words to say why it matters.</li>
        <li><b>Don't promise what the AI will say.</b> AI answers change every time. Write what you will try and what to look for, then react to what really happens.</li>
        <li><b>End with one thing to remember.</b> Skip the recap. Leave people with one takeaway or one thing to try.</li>
        <li><b>Read it out loud.</b> If you trip on a line or run out of breath, shorten it.</li>
        <li><b>Keep it real.</b> No made-up stories, quotes or numbers. Link every claim to where it came from.</li>
      </ol>
    </div>
  </section>

  <section class="block">
    <h2>What a script looks like <span class="tag">Example</span></h2>
    <div class="scriptex">
      <div class="ln spoken"><span class="lb">Spoken</span><p>For years, AI waited for you to type. That's changed.</p></div>
      <div class="ln visual"><span class="lb">On screen</span><p>A timeline of the tools that changed it.</p></div>
      <div class="ln spoken"><span class="lb">Spoken</span><p>Let's see what it does when I hand it a whole folder.</p></div>
      <div class="ln note"><span class="lb">Recording note</span><p>Open the demo folder. Run the prompt. Pause on whatever comes back.</p></div>
    </div>
  </section>

  <section class="block polish">
    <div>
      <h3>Your script is a draft</h3>
      <p class="pl2">Like a movie, a video gets polished three times. Nothing is set in stone until you publish, so improvise, rewrite and change things along the way.</p>
    </div>
    <div class="steps">
      <div class="st"><b>Write</b>You write it the way people read. That is a solid first draft.</div>
      <div class="st"><b>Record</b>Say it out loud and you hear what doesn't sound like you. Change it on the spot.</div>
      <div class="st"><b>Edit</b>AI clears the pauses and retakes. You look for ways to make it shorter and tighter.</div>
      <div class="st pub"><b>Publish</b>Now it's set.</div>
    </div>
  </section>

  <section class="block">
    <h2>Same idea, said out loud <span class="tag">A real before and after</span></h2>
    <div class="ba">
      <div class="col"><div class="bl">As I wrote it</div><p>In real life, the folks with the most PhDs don't always win. Usually it's the practical ones. The people who show up, work hard, and know how to get the job done. That's Gemini Flash. Not the valedictorian, not SOTA. It's the blue-collar model with the best tools in the shop. Not the brightest one in the room. Maybe the smartest choice.</p></div>
      <div class="col said"><div class="bl">As I said it on camera</div><p>I'm speaking from experience, almost all my applications use Gemini as the model inside. But like with people, the smartest models aren't always the most successful. It's the practical ones, the ones who show up, work hard, and know how to get the job done. That's the Gemini Flash family.</p></div>
      <div class="col why"><div class="bl">What changed</div><ul class="dots"><li>Added a real experience</li><li>Kept the core idea word for word</li><li>Dropped the lines that only work on paper</li><li>Ended sooner</li></ul></div>
    </div>
  </section>

  <section class="block">
    <h2>Organize and improve <span class="tag">Close the loop</span></h2>
    <div class="grid4w">
      <div><b>Organize it.</b> Turn your files into skills, like <a href="https://github.com/planetoftheweb/writing-companion">Writing Companion</a>. Use one Project per series. Keep it all in an editor like <a href="https://obsidian.md">Obsidian</a> and let Claude or ChatGPT update it.</div>
      <div><b>Build a performance rubric.</b> Pull your numbers from Publer or another social aggregator. Have AI turn your best posts into a rubric to check drafts against.</div>
      <div><b>Track time to relevance.</b> Count the days from "this topic matters" to "people can watch it." Speed and relevance go together.</div>
      <div><b>Keep the human parts.</b> Knowing what your audience needs right now, framing the question, and judging what is useful in practice.</div>
    </div>
  </section>

  <footer>Before and after example from my video on Google's Gemini Flash models, 2026.</footer>
</section>
"""

HTML = page("Writing for Video with AI", BODY)

if __name__ == "__main__":
    render("ai-video-writing-playbook", HTML)
