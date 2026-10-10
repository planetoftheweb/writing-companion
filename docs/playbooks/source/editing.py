"""Editing Video with AI: page content. Edit the HTML here, then run build.py."""
from common import page, render, BYLINE

HEART = "https://claude.ai/artifact/4XT7m3ePiNgqQXNgLnfKba"
DESCRIPT = "https://www.descript.com"
SNAGIT = "https://www.techsmith.com/snagit/"
PIXTAFFY = "https://pixtaffy.com"
CLAUDE = "https://claude.ai"
CHATGPT = "https://chatgpt.com"
SMART = "https://help.descript.com/effects-animations-transitions/smart-transitions"
EXTRA = r"""
  a { color: var(--teal); font-weight: 700; text-decoration: none; border-bottom: 0.75pt solid rgba(15,143,128,.45); }
  .gallery { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12pt 12pt; }
  .tile .img { border-radius: 6pt; overflow: hidden; border: 1pt solid var(--line); aspect-ratio: 16 / 9; position: relative; }
  .tile .img img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .tile .kind { font-size: 6.4pt; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--teal); margin: 5pt 0 1pt; }
  .tile h3 { font-size: 9.4pt; margin-bottom: 2pt; }
  .tile p { font-size: 7.9pt; line-height: 1.36; }
  .tools { background: var(--teal-soft); border-radius: 6pt; padding: 9pt 11pt; }
  .tools h3 { margin-bottom: 5pt; }
  .tools ul { list-style: none; }
  .tools li { font-size: 8pt; margin-bottom: 5pt; line-height: 1.35; }
  .tryit { margin-top: 10pt; }
  ul.dots { list-style: none; }
  ul.dots li { position: relative; padding-left: 10pt; margin-bottom: 5pt; }
  ul.dots li::before { content: ""; position: absolute; left: 0; top: 4.5pt; width: 5pt; height: 5pt; border-radius: 1.5pt; background: var(--teal); }
  .yours { background: var(--chip); border-radius: 6pt; padding: 8pt 10pt; margin-top: 8pt; }
  .yours h3 { margin-bottom: 4pt; }
  .grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0 14pt; font-size: 8pt; }
  .grid4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0 12pt; font-size: 8pt; }
  .grid4 b, .grid3 b { display: block; margin-bottom: 2pt; }

  .polish { display: grid; grid-template-columns: 1.9in 1fr; gap: 12pt; align-items: center; background: var(--chip); border-radius: 7pt; padding: 8pt 10pt; }
  .polish h3 { font-size: 10.5pt; margin-bottom: 2pt; }
  .polish .pl2 { font-size: 7.9pt; color: var(--muted); line-height: 1.35; }
  .polish .steps { display: grid; grid-template-columns: 1fr 1fr 1fr 0.55fr; gap: 6pt; align-items: stretch; }
  .polish .st { background: #fff; border-radius: 5pt; padding: 5pt 7pt; font-size: 7.7pt; line-height: 1.33; position: relative; }
  .polish .st b { display: block; font-size: 8.6pt; color: var(--teal); margin-bottom: 1pt; }
  .polish .st.pub { background: var(--ink); color: #fff; display: flex; flex-direction: column; justify-content: center; }
  .polish .st.pub b { color: #fff; }
  .polish .st:not(.pub)::after { content: "\203A"; position: absolute; right: -6pt; top: 50%; transform: translateY(-50%); color: var(--muted); font-size: 11pt; font-weight: 700; }
  .extras { font-size: 8.4pt; margin: 2pt 0 7pt; }
  body { font-size: 9pt; line-height: 1.4; }
  .tile p, .tools li, .grid3, .grid4, .checks div, .prompt .pt { font-size: 8.4pt; }
  .lead { font-size: 8.6pt; }
  section.block { margin-bottom: 13pt; }
  ol.rules li { margin-bottom: 6.5pt; }
"""

BODY = f"""

<!-- ============================ PAGE 1 ============================ -->
<section class="page">
  <header>
    <div>
      <div class="kicker">Video playbook</div>
      <h1>Editing Video with AI</h1>
      <p class="sub">Plain steps for your first video or your hundredth. I edit in <a href="{DESCRIPT}">Descript</a>. Most editors now have similar AI tools, so look for the same features in yours.</p>
    </div>
    {BYLINE}
  </header>

  <section class="stats">
    <div class="stat"><div class="v">Minutes</div><div class="l"><b>For a rough cut</b> that used to take a full day.</div></div>
    <div class="stat"><div class="v">41 to 7</div><div class="l"><b>Minutes recorded</b> to minutes published on a recent video.</div></div>
    <div class="stat"><div class="v">4 clicks</div><div class="l"><b>Of AI cleanup</b> on every recording before I read a word.</div></div>
    <div class="stat"><div class="v">3x</div><div class="l"><b>More videos, same hours.</b> 2 to 3 short videos a week.</div></div>
  </section>

  <section class="block polish">
    <div>
      <h3>Polish it three times</h3>
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
    <h2>Record like you're editing <span class="tag">The edit starts at the mic</span></h2>
    <div class="two">
      <ol class="rules">
        <li><b>Plan what you'll show.</b> Attention spans are short. Before you hit record, decide what is on screen for each part: a demo, a chart or a screenshot.</li>
        <li><b>Pause between ideas.</b> A one second pause gives you a clean spot to cut or to start a new scene.</li>
        <li><b>Flub a line? Start the sentence over.</b> Pause, then say the whole sentence again. AI cleanup spots full restarts easily. Fixes in the middle of a sentence are harder for it to catch.</li>
      </ol>
      <ol class="rules start4">
        <li><b>Record your screen and camera together.</b> The demo shows the proof. Your face keeps it personal.</li>
        <li><b>Record more than you need.</b> My recordings run five to six times longer than the final video. That is normal.</li>
        <li><b>Save the intro and outro for last.</b> Once you know what the video says, they are easy. Re-recorded bits like these are called pickups.</li>
      </ol>
    </div>
  </section>

  <section class="block passes">
    <div>
      <div class="shot"><img src="img/descript-passes.png" alt="Descript AI tools menu with four tools numbered in the order used"></div>
      <p class="cap">Descript's AI tools, numbered in the order I use them.</p>
    </div>
    <div>
      <h2>Let AI do the first cleanup <span class="tag">One click each</span></h2>
      <p style="margin-bottom:5pt;">Descript turns your video into a transcript. Delete a word and the video cuts with it. These four tools do the first round of cleanup. Run them before you read anything.</p>
      <ol class="order">
        <li><b>Shorten word gaps.</b> Trims long pauses. I trim anything over 1 second.</li>
        <li><b>Remove retakes.</b> Finds where you started a sentence over and removes the extra take.</li>
        <li><b>Edit for clarity.</b> Trims rambling and repeats. I use the medium setting.</li>
        <li><b>Add chapters.</b> Labels each section so you can jump around fast.</li>
      </ol>
      <p class="extras"><b>Also worth a click:</b> Studio Sound makes a home microphone sound like a studio. Remove filler words cuts the ums and uhs.</p>
      <div class="tip"><b>Using another editor?</b> Look for the same tools: silence removal, retake detection, an AI cleanup pass and automatic chapters.</div>
    </div>
  </section>

  <footer>Rough cut time, output and recording lengths come from my own projects in 2026.</footer>
</section>

<!-- ============================ PAGE 2 ============================ -->
<section class="page">
  <div class="runhead"><span>Editing Video with AI</span><span>Page 2</span></div>

  <section class="block">
    <h2>Make it shorter <span class="tag">Your job in the edit</span></h2>
    <p class="lead">AI cleanup clears the pauses and retakes. Your job is to make the video tighter. Read the transcript and look for these.</p>
    <div class="two">
      <ol class="rules">
        <li><b>Long setup.</b> Get to the good part faster. If the demo starts two minutes in, start it sooner.</li>
        <li><b>Explaining what's on screen.</b> People can see what you click. Keep the why and cut the play-by-play.</li>
        <li><b>The same idea twice.</b> You said it again later in different words. Keep the stronger one.</li>
      </ol>
      <ol class="rules" style="counter-reset: n 3;">
        <li><b>Side trips.</b> A detour that doesn't serve the one point. Cut it or save it for another video.</li>
        <li><b>Extra words.</b> "In this video," "let me show you," "sorry, hold on." Cut them and keep the sentence.</li>
        <li><b>A quiet screen.</b> Twenty seconds with nothing new to see. Trim it, add a visual or re-record it shorter.</li>
      </ol>
    </div>
  </section>

  <section class="block">
    <h2>Ask the AI editor for a to-do list <span class="tag">Underlord, Descript's AI editor</span></h2>
    <p class="lead">Ask for a report first. Pick what you want. Then let it cut. Claude or ChatGPT can fill in these prompts with your details.</p>
    <div class="two" style="gap: 7pt 12pt;">
      <div class="prompt"><div class="pl">Step 1. Ask for a report</div><div class="pt">Don't edit anything yet. Read my transcript and watch the screen recording. List the time and the exact words for anything I said twice, sentences that start mid-thought, phrases like "in this video," names or web addresses spelled wrong in the captions, spots I should re-record, and lines I could say in fewer words. My recording is correct even where it differs from my script.</div></div>
      <div class="prompt"><div class="pl">Step 2. Approve the cuts</div><div class="pt">Delete only the items below, word for word. Don't reword anything, add anything or create new audio. When you finish, list what changed and tell me if anything else was removed.<br>1. Delete: "[exact words]"<br>2. Delete: "[exact words]"</div></div>
    </div>
    <div class="yours">
      <h3>Keep these jobs for yourself</h3>
      <div class="grid3">
        <div><b>Tiny cuts.</b> Ask an AI to cut one or two words and it may take the whole phrase. Do those by hand.</div>
        <div><b>Your voice.</b> Fix caption typos by editing the text. Don't generate new audio to fix a word.</div>
        <div><b>The final check.</b> Read the transcript after every AI edit. A fix counts once you see it.</div>
      </div>
    </div>
  </section>

  <section class="block">
    <h2>Make it look finished <span class="tag">Small touches that add up</span></h2>
    <div class="two">
      <ol class="rules">
        <li><b><a href="{SMART}">Smart transitions</a>.</b> Descript adds a smooth move between scenes for you. Set them once in your layouts and every new scene gets them.</li>
        <li><b>Layouts.</b> Build a few once: a title card, a name plate, screen with camera, and a web address bar. Reuse them on every video. On a layout with a web address, turn off Smart Fill so it keeps your exact address.</li>
        <li><b>Zoom in on what matters.</b> When you highlight something on screen, zoom in while you talk about it, then zoom back out. The AI editor can add zooms and callouts for you.</li>
      </ol>
      <ol class="rules start4">
        <li><b>Show the web address.</b> The first time a website appears, put its address on screen so people can find it.</li>
        <li><b>Start new scenes with a slash.</b> Type / in the script to start a new scene. Give each pickup its own scene so the new take drops right in.</li>
        <li><b>Add captions.</b> Descript can highlight each word as you say it. Fix any misspelled names in the text before you export.</li>
      </ol>
    </div>
  </section>

  <section class="block">
    <h2>Before you export <span class="tag">Quick checklist</span></h2>
    <div class="checks">
      <div>Names and web addresses in the captions are spelled right.</div>
      <div>Chapter titles match what you say in each section.</div>
      <div>The video ends on a clear closing line.</div>
      <div>No 20 second stretch goes by with nothing new on screen.</div>
      <div>Your re-recorded intro and outro are in place.</div>
      <div>Captions checked again after pickups. New takes bring new typos.</div>
    </div>
  </section>

  <footer>Underlord, Studio Sound, Smart transitions and the other tools named here are Descript features. Prompts condensed from my own editing workflow.</footer>
</section>

<!-- ============================ PAGE 3 ============================ -->
<section class="page">
  <div class="runhead"><span>Editing Video with AI</span><span>Page 3</span></div>

  <section class="block">
    <h2>Visuals you can make in minutes <span class="tag">Give every part something to see</span></h2>
    <div class="gallery">
      <div class="tile">
        <div class="img"><img src="img/heart-frame.jpg" alt="Frame from an animated heart explainer built with Claude"></div>
        <div class="kind">Motion graphic</div>
        <h3>Animated explainers from a prompt</h3>
        <p><a href="{CLAUDE}">Claude</a> built this 20 second animated explainer from one short prompt. <a href="{HEART}">Watch it here</a>. Play it full screen, record it and drop it in.</p>
      </div>
      <div class="tile">
        <div class="img"><img src="img/bars.jpg" alt="3D bar chart comparing 41 minutes recorded with 7 minutes published"></div>
        <div class="kind">Chart overlay</div>
        <h3>Charts that sit on your video</h3>
        <p>Export a chart as a video with a see-through background. It plays right on top of your recording.</p>
      </div>
      <div class="tile">
        <div class="img"><img src="img/infographic.jpg" alt="Hand-drawn style infographic about AI agents"></div>
        <div class="kind">Infographic</div>
        <h3>One paragraph in, one graphic out</h3>
        <p>Describe the idea and let an image tool draw it. <a href="{PIXTAFFY}">PixTaffy</a> makes graphics like this, and <a href="{CHATGPT}">ChatGPT</a> has one of the best image generators out there.</p>
      </div>
      <div class="tile">
        <div class="img"><img src="img/mock-stock.jpg" alt="Stock video thumbnail of a city skyline at sunset with a play button"></div>
        <div class="kind">Stock video</div>
        <h3>B-roll without a camera</h3>
        <p>Descript has stock video built in. Search, drag it in, and use it to open a section or cover a voice-over.</p>
      </div>
      <div class="tile">
        <div class="img"><img src="img/mock-snagit.jpg" alt="Screenshot of a settings page with a numbered marker, a highlight box and an arrow"></div>
        <div class="kind">Screenshot with callouts</div>
        <h3>Point at exactly what matters</h3>
        <p><a href="{SNAGIT}">Snagit</a> grabs quick screenshots and short screen clips. Add numbers, arrows and highlights, then paste them into Descript.</p>
      </div>
      <div class="tools">
        <h3>Tools on this page</h3>
        <ul class="dots">
          <li><a href="{DESCRIPT}">Descript</a> for editing, AI cleanup, stock video and vertical clips</li>
          <li><a href="{CLAUDE}">Claude</a> for motion graphics and writing your AI prompts</li>
          <li><a href="{CHATGPT}">ChatGPT</a> for generated images</li>
          <li><a href="{PIXTAFFY}">PixTaffy</a> for infographics in your brand style</li>
          <li><a href="{SNAGIT}">Snagit</a> for screenshots, callouts and quick clips</li>
        </ul>
      </div>
    </div>
    <div class="prompt tryit"><div class="pl">Try it: a motion graphic prompt for Claude</div><div class="pt">Create a 20 second motion graphic that explains [your idea] in four short scenes: a bold title, the problem, how it works, and one key number. Dark background, bright accent colors, kinetic type. SVG and CSS only, in a single HTML file that plays and loops on its own.</div></div>
  </section>

  <section class="block">
    <h2>One recording, many videos <span class="tag">Reuse everything</span></h2>
    <div class="grid4">
      <div><b>Go vertical.</b> Descript reformats a horizontal video into a vertical one for phones.</div>
      <div><b>Cut short clips.</b> The AI editor finds your strongest moments and trims them to a length you pick. Each clip makes one point.</div>
      <div><b>Post with it.</b> A companion post reflects what's in the video, teases what people will see, and gives one useful takeaway on its own. Then link to the video. Start from this <a href="https://github.com/planetoftheweb/writing-companion/tree/main/skills/writing-companion/assets/content-types/linkedin-post">post format</a>.</div>
      <div><b>Save the final transcript.</b> Keep it next to your script. Comparing the two shows how you really talk, so your next script sounds more like you.</div>
    </div>
  </section>

  <section class="block">
    <h2>Your editing workflow <span class="tag">Start to finish</span></h2>
    <div class="flow">
      <div><i>1</i><b>Plan</b> what you'll show</div>
      <div><i>2</i><b>Record</b> with pauses and full restarts</div>
      <div><i>3</i><b>Run AI cleanup</b> in order</div>
      <div><i>4</i><b>Make it shorter</b> by reading the transcript</div>
      <div><i>5</i><b>Get the AI report,</b> then approve cuts</div>
      <div><i>6</i><b>Record pickups</b> for the intro, outro and fixes</div>
      <div><i>7</i><b>Polish</b> with layouts, zooms and visuals</div>
      <div><i>8</i><b>Run the checklist</b></div>
      <div><i>9</i><b>Export</b> long, vertical and clips</div>
    </div>
  </section>

  <footer>Links: Descript descript.com. Snagit techsmith.com/snagit. PixTaffy pixtaffy.com. Claude claude.ai. ChatGPT chatgpt.com. Stock video and screenshot examples on this page are mockups.</footer>
</section>
"""

HTML = page("Editing Video with AI", BODY, EXTRA)

if __name__ == "__main__":
    render("ai-video-editing-playbook", HTML)
