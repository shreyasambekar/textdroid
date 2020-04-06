package com.renard.ocr.documents.creation;

import com.googlecode.tesseract.android.OCR;
import com.renard.ocr.MonitoredActivity;
import com.renard.ocr.R;
import com.renard.ocr.documents.creation.crop.CropImageActivity;
import com.renard.ocr.documents.creation.visualisation.OCRActivity;
import com.renard.ocr.documents.creation.NewDocumentActivity;
import com.renard.ocr.documents.viewing.DocumentContentProvider;
import com.renard.ocr.documents.viewing.DocumentContentProvider.Columns;
import com.renard.ocr.documents.viewing.grid.DocumentGridActivity;
import com.renard.ocr.documents.viewing.single.DocumentActivity;
import com.renard.ocr.pdf.Hocr2Pdf;
import com.renard.ocr.pdf.Hocr2Pdf.PDFProgressListener;
import com.renard.ocr.util.MemoryInfo;
import com.renard.ocr.util.Util;

import android.annotation.TargetApi;
import android.app.Activity;
import android.app.AlertDialog;
import android.app.AlertDialog.Builder;
import android.app.Dialog;
import android.app.ProgressDialog;
import android.content.ActivityNotFoundException;
import android.content.BroadcastReceiver;
import android.content.ContentProviderClient;
import android.content.ContentValues;
import android.content.Context;
import android.content.DialogInterface;
import android.content.DialogInterface.OnClickListener;
import android.content.Intent;
import android.content.IntentFilter;
import android.database.Cursor;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.os.RemoteException;
import android.provider.MediaStore;
import android.support.v4.app.DialogFragment;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.content.FileProvider;
import android.support.v4.content.LocalBroadcastManager;
import android.support.v4.view.accessibility.AccessibilityManagerCompat;
import android.text.Html;
import android.text.Spanned;
import android.util.Log;
import android.util.Pair;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.accessibility.AccessibilityManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;

import static com.renard.ocr.documents.creation.NewDocumentActivity.EXTRA_NATIVE_PIX;
import static com.renard.ocr.documents.creation.NewDocumentActivity.UPLOAD_IMAGE;

/*  Created by: Shreyas Ambekar on
        April 1, 2020
* */

public class ImageUploadDialog extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setMessage("Upload image?");
        builder.setTitle("Upload image?");
        builder.setNegativeButton("No", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                Bundle extras = getIntent().getExtras();
                long nativePix = extras.getLong(EXTRA_NATIVE_PIX,  0);
                boolean accessibilityMode = extras.getBoolean(OCRActivity.EXTRA_USE_ACCESSIBILITY_MODE, false);
                Intent result = new Intent();
                result.putExtra(UPLOAD_IMAGE, false);
                result.putExtra(EXTRA_NATIVE_PIX, nativePix);
                result.putExtra(OCRActivity.EXTRA_USE_ACCESSIBILITY_MODE, accessibilityMode);
                setResult(RESULT_OK, result);
                finish();
            }
        });

        builder.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                Bundle extras = getIntent().getExtras();
                long nativePix = extras.getLong(EXTRA_NATIVE_PIX,  0);
                boolean accessibilityMode = extras.getBoolean(OCRActivity.EXTRA_USE_ACCESSIBILITY_MODE, false);
                Intent result = new Intent();
                result.putExtra(UPLOAD_IMAGE, true);
                result.putExtra(EXTRA_NATIVE_PIX, nativePix);
                result.putExtra(OCRActivity.EXTRA_USE_ACCESSIBILITY_MODE, accessibilityMode);
                setResult(RESULT_OK, result);
                finish();
            }
        });
        AlertDialog alert = builder.create();
        alert.setCanceledOnTouchOutside(false);
        alert.show();
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
        setResult(RESULT_CANCELED);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
    }

}