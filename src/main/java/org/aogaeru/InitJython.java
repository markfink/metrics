package org.testingsoftware.metrics;

// import javax.script.ScriptEngine;
// import javax.script.ScriptEngineManager;
// import javax.script.ScriptException;
import org.python.core.Py;
// import org.python.core.PyFile;
import org.python.core.PySystemState;
import org.python.util.InteractiveConsole;
import java.util.Properties;

import org.apache.commons.lang.StringUtils;

public class InitJython {

	public static void main(String[] args) {
		// System.out.println("Java started");
		// System.out.print(args.length + " Arguments: ");
		// for (String s : args) {
		// 	System.out.print(s);
		// 	System.out.print(", ");
		// }
		// System.out.println();

		PySystemState.initialize(PySystemState.getBaseProperties(),
			new Properties(), args);
		// PySystemState systemState = Py.getSystemState();
		// systemState.ps1 = systemState.ps2 = Py.EmptyString;
		InteractiveConsole c = new InteractiveConsole();
		Py.getSystemState().__setattr__("_jy_interpreter", Py.java2py(c));
        // ScriptEngine engine = new ScriptEngineManager().getEngineByName("python");

		c.exec("try:\n  from metrics.metrics import main\n  main()\nexcept SystemExit:\n  pass");
		// engine.eval("from metrics.metrics import main");
		// engine.eval("main('" + StringUtils.join(args, " ") + "')");
		System.out.println("Java exiting");
	}

	// public void run() throws ScriptException {
	// }
}

		// if (args.length > 0) {
		// 	if (args[0].equals("eval"))
		// 		if (args.length > 1)
		// 			c.exec(args[1]);
		// 		else
		// 			c.exec("try:\n import fibcalc\n fibcalc.main()\nexcept SystemExit: pass");
		// 	else if (args[0].equals("run"))
		// 		if (args.length > 1)
		// 			c.execfile(args[1]);
		// 		else
		// 			c.execfile(InitJython.class
		// 					.getResourceAsStream("Lib/fibcalc/__init__.py"),
		// 					"fibcalc/__init__.py");
		// 	else if (args[0].equals("script")) {
		// 		String engineName = args[1];
		// 		ScriptEngine eng = new ScriptEngineManager()
		// 				.getEngineByName(engineName);
		// 		if (eng == null) {
		// 			throw new NullPointerException("Script Engine '"
		// 					+ engineName + "' not found!");
		// 		}
		// 		eng.put("engine", engineName);
		// 		if (args.length > 2) {
		// 			System.out.println("result: " + eng.eval(args[2]));
		// 		} else {
		// 			System.out.println("write your script below; terminate "
		// 					+ "with Ctrl-Z (Windows) or Ctrl-D (Unix) ---");
		// 			try {
		// 				System.out.println("result: "
		// 						+ eng.eval(new InputStreamReader(
		// 								new ConsoleReader().getInput())));
		// 			} catch (IOException e) {
		// 				e.printStackTrace();
		// 			}
		// 		}
		// 	} else
		// 		System.out
		// 				.println("use either eval or run or script as first argument");
		// } else
		// 	c.interact();
