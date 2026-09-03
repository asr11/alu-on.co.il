export default {
  async fetch(request, env) {
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    if (request.method === "POST") {
      try {
        const body = await request.json();
        const { 
          name, phone, service, notes, 
          gclid, utm_source, utm_campaign, utm_medium, 
          landing_path, session_id 
        } = body;

        const stmt = env.DB.prepare(
          `INSERT INTO leads 
          (name, phone, service, notes, gclid, utm_source, utm_campaign, utm_medium, landing_path, session_id) 
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
        ).bind(
          name || null, phone || null, service || null, notes || null,
          gclid || null, utm_source || null, utm_campaign || null, utm_medium || null,
          landing_path || null, session_id || null
        );
        
        await stmt.run();

        return new Response(JSON.stringify({ success: true }), {
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      } catch (err) {
        return new Response(JSON.stringify({ error: err.message }), {
          status: 500,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }
    }

    return new Response("Not Found", { status: 404 });
  }
};
