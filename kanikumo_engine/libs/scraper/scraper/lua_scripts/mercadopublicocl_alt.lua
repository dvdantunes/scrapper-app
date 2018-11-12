function wait_for_element(splash, css, maxwait)
  -- Wait until a selector matches an element in the page.
  -- Return an error if waited more than maxwait seconds.

  if maxwait == nil then
      maxwait = 5
  end

  return splash:wait_for_resume(string.format([[
    function main(splash) {
      var selector = '%s';
      var maxwait = %s;
      var end = Date.now() + maxwait*1000;

      function check() {
        if(document.querySelector(selector)) {
          splash.resume('Element found');
        } else if(Date.now() >= end) {
          var err = 'Timeout waiting for element';
          splash.error(err + " " + selector);
        } else {
          setTimeout(check, 200);
        }
      }
      check();
    }
  ]], css, maxwait))
end


function no_items(splash, error_msg)
  -- Responser helper in case no errores were found

  return {
    error = 0,
    error_msg = error_msg,
    page1 = {hmtl = ''},
    page2 = {hmtl = ''},
    performance = splash:get_perf_stats()
  }
end


function error(splash, reason, error_msg)
  -- Responser helper in case of error

  return {
    error = 1,
    error_msg = error_msg,
    reason = reason,
    performance = splash:get_perf_stats()
  }
end


function main(splash)
  -- Try to get 2 pages of big purchases from mercadopublico.cl

  -- Initial config
  splash.js_enabled = %(js_enabled)s
  splash.images_enabled = %(images_enabled)s
  splash.webgl_enabled = %(webgl_enabled)s
  splash.media_source_enabled = %(media_source_enabled)s
  splash.set_user_agent('%(user_agent)s')


  -- First request
  assert(splash:go(splash.args.url))
  --assert(splash:wait(0.5))


  -- Set dates and submit form
  result, error = wait_for_element(splash, '#heaFecha label[for=chkFecha]')
  if not result then
    return error(splash, 'no-date-checkbox', error)
  end

  assert(splash:runjs("document.querySelector('#heaFecha label[for=chkFecha]').click();"))
  --assert(splash:wait(0.2))

  result, error = wait_for_element(splash, '#txtFecha1')
  if not result then
    return error(splash, 'no-input-txtFecha1', error)
  end

  result, error = wait_for_element(splash, '#txtFecha2')
  if not result then
    return error(splash, 'no-input-txtFecha2', error)
  end

  result, error = wait_for_element(splash, '#btnBusqueda')
  if not result then
    return error(splash, 'no-button-btnBusqueda', error)
  end

  assert(splash:runjs("document.querySelector('#txtFecha1').value = '%(last_60_days)s';"))
  assert(splash:runjs("document.querySelector('#txtFecha2').value = '%(today)s';"))
  assert(splash:runjs("document.querySelector('#btnBusqueda').click();"))


  -- Waits for javascript to load on next page
  assert(splash:wait(1.5))


  -- Are there any items?
  result, error = wait_for_element(splash, '#pnlSearch1 table')
  if not result then
    return no_items(splash, error)
  end
  --local no_items = splash.evaljs("document.querySelector('#lblSearchCountAcquisition') ? 1 : 0")


  -- Prepares result data
  local returnData = {
    error = 0,
    no_items = 1
  }


  -- Waits for 'back button' to render
  result, error = wait_for_element(splash, '#ImageButton1')
  if not result then
    return error(splash, 'no-button-ImageButton1', error)
  end


  -- Get page 1 results
  returnData['page1'] = {html = splash:html()}--, png = splash:png()}


  -- Check paginator #2 and get page 2 results
  local paginator = splash:evaljs("document.querySelector('#PaginadorBusqueda__TblPages td:nth-child(3) div') ? 1 : 0")
  if paginator then
    assert(splash:runjs("document.querySelector('#PaginadorBusqueda__TblPages td:nth-child(3) div').click();"))

    -- Waits for javascript to load on next page
    assert(splash:wait(1.5))


    -- Waits for 'back button' to render
    result, error = wait_for_element(splash, '#ImageButton1')
    if not result then
      return error(splash, 'no-button-ImageButton1-2', error)
    end

    returnData['page2'] = {html = splash:html()}--, png = splash:png()}

  else
    returnData['page2'] = {html = ''}--, png = splash:png()}
  end


  -- Get performance stats
  returnData['performance'] = splash:get_perf_stats()

  return returnData
end
