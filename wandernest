
            subtotal = hotel_cost + transport_cost + food_cost + activity_cost + breakfast_cost + insurance_cost + guided_cost
            estimated_tax = subtotal * 0.05
            total_cost = subtotal + estimated_tax
            per_person_cost = total_cost / int(travellers)

            # The conditional suggests a budget status based on the per-person estimate.
            if per_person_cost < 10000:
                budget_label = "Budget-friendly"
                budget_message = "Your choices keep the estimated per-person cost on the lower side."
            elif per_person_cost < 25000:
                budget_label = "Balanced trip"
                budget_message = "This estimate sits in a mid-range travel budget."
            else:
                budget_label = "Premium experience"
                budget_message = "Your selected options create a higher-comfort travel estimate."

            st.divider()
            st.markdown('<div class="section-kicker">Your estimate</div>', unsafe_allow_html=True)
            st.header(f"{destination}: your trip at a glance")
            metric_one, metric_two, metric_three = st.columns(3)
            metric_one.metric("Estimated total", f"₹{total_cost:,.0f}")
            metric_two.metric("Per person", f"₹{per_person_cost:,.0f}")
            metric_three.metric("Trip length", f"{int(trip_days)} days")

            st.success(f"**{budget_label}** — {budget_message}")
            st.caption(
                f"Departure: {departure_date.strftime('%d %B %Y')} · "
                f"{int(travellers)} traveller(s) · {rooms_needed} room(s) estimated"
            )

            # A simple table makes the arithmetic transparent to the user.
            breakdown = [
                ("Accommodation", hotel_cost),
                ("Round-trip transport", transport_cost),
                ("Food estimate", food_cost),
                ("Standard activities", activity_cost),
                ("Breakfast add-on", breakfast_cost),
                ("Travel insurance", insurance_cost),
                ("Guided experiences", guided_cost),
                ("Illustrative tax / buffer (5%)", estimated_tax),
                ("TOTAL ESTIMATE", total_cost),
            ]
            st.subheader("Where your budget goes")
            for label, amount in breakdown:
                left, right = st.columns([3, 1])
                left.write(f"**{label}**" if label == "TOTAL ESTIMATE" else label)
                right.markdown(f"<div style='text-align:right;font-weight:{'800' if label == 'TOTAL ESTIMATE' else '500'}'>₹{amount:,.0f}</div>", unsafe_allow_html=True)

            st.caption(
                "Planning estimate only. Rates are illustrative and do not represent live hotel, transport, "
                "activity, insurance or tax quotations. Accommodation is estimated per room per night."
            )

            # Build a personalised itinerary using the selected destination and trip length.
            st.divider()
            st.markdown('<div class="section-kicker">Made for your getaway</div>', unsafe_allow_html=True)
            st.subheader("Suggested itinerary")
            day_ideas = destination_info["itinerary"]
            for day_number in range(1, int(trip_days) + 1):
                idea = day_ideas[(day_number - 1) % len(day_ideas)]
                st.markdown(
                    f"<div class='info-box' style='margin-bottom:.6rem'><strong>Day {day_number}</strong>"
                    f"<br><span style='color:#526777'>{idea}</span></div>",
                    unsafe_allow_html=True,
                )

            # Provide a plain-text trip summary the user can download.
            summary_lines = [
                "WANDERNEST TRAVELS — TRIP PLAN",
                f"Destination: {destination}",
                f"Departure date: {departure_date.strftime('%d %B %Y')}",
                f"Travellers: {int(travellers)}",
                f"Duration: {int(trip_days)} days",
                f"Stay preference: {hotel_category}",
                f"Main transport: {transport}",
                "",
                "ESTIMATED COST BREAKDOWN",
            ]
            summary_lines.extend([f"{label}: INR {amount:,.0f}" for label, amount in breakdown])
            summary_lines.extend(["", "SUGGESTED ITINERARY"])
            summary_lines.extend([f"Day {day_number}: {day_ideas[(day_number - 1) % len(day_ideas)]}" for day_number in range(1, int(trip_days) + 1)])
            summary_lines.extend(["", "Note: Estimates are illustrative, not live quotations."])
            st.download_button(
                "⬇️ Download my trip plan",
                data="\n".join(summary_lines),
                file_name="wandernest_trip_plan.txt",
                mime="text/plain",
                use_container_width=True,
            )

    except (ValueError, TypeError, ZeroDivisionError) as error:
        # Catch common input/calculation errors and show a helpful message instead of crashing.
        st.error(f"We couldn't calculate this trip. Please review your selections and try again. ({error})")

st.write("")
st.divider()
footer_left, footer_right = st.columns([2, 1])
with footer_left:
    st.markdown("**WANDERNEST TRAVELS**  ·  Plan better. Travel further.")
    st.caption("A student Python project created to demonstrate interactive business calculations.")
with footer_right:
    st.markdown("<div style='text-align:right;color:#647987;font-size:.8rem'>Explore thoughtfully. Travel confidently. 🌿</div>", unsafe_allow_html=True)
